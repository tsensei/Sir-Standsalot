import discord
from discord import app_commands
import json
import os
from datetime import datetime
from config import TIMEZONE, STANDUP_START_HOUR, STANDUP_START_MINUTE, STANDUP_END_HOUR, STANDUP_END_MINUTE


def register_slash_commands(bot):
    """Register slash commands for the bot"""

    @bot.tree.command(name="attendance", description="Check current standup attendance")
    async def attendance_slash(interaction: discord.Interaction):
        """Check current standup attendance"""
        if bot.is_standup_active:
            current = await bot.tracker.track_attendance()
            if current:
                names = [m['name'] for m in current]
                embed = discord.Embed(
                    title="📊 Current Attendance",
                    description=f"**In Voice Channel:** {len(names)}\n\n" +
                               "\n".join(f"• {name}" for name in names),
                    color=discord.Color.blue()
                )
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("No one is currently in the standup channel.")
        else:
            await interaction.response.send_message("Standup is not currently active.")

    @bot.tree.command(name="async_check", description="Check today's async updates")
    async def async_check_slash(interaction: discord.Interaction):
        """Check today's async updates"""
        await interaction.response.defer()

        updates = await bot.tracker.check_day_highlights()
        if updates:
            embed = discord.Embed(
                title="📝 Today's Async Updates",
                description=f"Found {len(updates)} updates before cutoff",
                color=discord.Color.green()
            )

            for user_id, data in list(updates.items())[:10]:
                embed.add_field(
                    name=f"{data['name']} at {data['time']}",
                    value=data['message'][:100] + "..." if len(data['message']) > 100 else data['message'],
                    inline=False
                )

            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("No async updates found for today before cutoff time.")

    @bot.tree.command(name="standup_stats", description="Get standup statistics")
    @app_commands.describe(days="Number of days to include (default: 7)")
    async def standup_stats_slash(interaction: discord.Interaction, days: int = 7):
        """Get standup statistics for the last N days"""
        await interaction.response.defer()

        # Load attendance records
        current_month = datetime.now(TIMEZONE).strftime("%Y_%m")
        filename = f'data/attendance_{current_month}.json'

        if not os.path.exists(filename):
            await interaction.followup.send("No attendance data available yet.")
            return

        with open(filename, 'r') as f:
            records = json.load(f)

        # Get last N days of records
        recent_records = records[-days:] if len(records) > days else records

        if not recent_records:
            await interaction.followup.send("No records found.")
            return

        # Calculate statistics
        total_voice = sum(r['voice_count'] for r in recent_records)
        total_async = sum(r['async_count'] for r in recent_records)
        avg_participation = sum(r['total_participation'] for r in recent_records) / len(recent_records)

        embed = discord.Embed(
            title=f"📈 Standup Statistics (Last {len(recent_records)} days)",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Summary",
            value=f"**Total Voice Attendance:** {total_voice}\n"
                  f"**Total Async Updates:** {total_async}\n"
                  f"**Avg. Participation:** {avg_participation:.1f}",
            inline=False
        )

        # Add daily breakdown
        daily_summary = []
        for record in recent_records[-5:]:  # Last 5 days
            date = record['date']
            voice = record['voice_count']
            async_count = record['async_count']
            daily_summary.append(f"`{date}`: 🎙️ {voice} | 📝 {async_count}")

        if daily_summary:
            embed.add_field(
                name="Recent Days",
                value="\n".join(daily_summary),
                inline=False
            )

        await interaction.followup.send(embed=embed)

    @bot.tree.command(name="test_standup", description="Test standup manually (Admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def test_standup_slash(interaction: discord.Interaction):
        """Test standup manually (Admin only)"""
        from src.core.utils import start_standup, end_standup
        import asyncio

        if not bot.is_standup_active:
            bot.is_standup_active = True

            # Check for async updates first
            await interaction.response.send_message("🔍 Checking for async updates...")
            bot.tracker.async_updates_today = await bot.tracker.check_day_highlights()

            # Send status message
            async_count = len(bot.tracker.async_updates_today)
            await interaction.followup.send(
                f"✅ Found {async_count} async update(s)\n"
                f"⏱️ Standup test started! Will end in 30 seconds..."
            )

            await start_standup(bot)

            # Auto-end after 30 seconds for testing
            await asyncio.sleep(30)
            await end_standup(bot)
            bot.is_standup_active = False
        else:
            await interaction.response.send_message("⚠️ Standup is already active!")

    @bot.tree.command(name="help", description="Show standup bot commands and information")
    async def help_slash(interaction: discord.Interaction):
        """Show help for standup bot commands"""
        embed = discord.Embed(
            title="🤖 Standup Bot Commands",
            description="Here are all available commands:",
            color=discord.Color.green()
        )

        commands_list = [
            ("</attendance:0>", "Check current standup attendance"),
            ("</async_check:0>", "View today's async updates"),
            ("</standup_stats:0>", "Get statistics for last N days (default: 7)"),
            ("</test_standup:0>", "Test standup manually (Admin only)"),
            ("</help:0>", "Show this help message")
        ]

        for cmd, desc in commands_list:
            embed.add_field(name=cmd, value=desc, inline=False)

        embed.add_field(
            name="📅 Schedule",
            value=f"**Daily Standup:** {STANDUP_START_HOUR:02d}:{STANDUP_START_MINUTE:02d} - "
                  f"{STANDUP_END_HOUR:02d}:{STANDUP_END_MINUTE:02d} (Asia/Dhaka)\n"
                  f"**Async Cutoff:** {STANDUP_START_HOUR:02d}:{STANDUP_START_MINUTE:02d}",
            inline=False
        )

        embed.add_field(
            name="📝 Async Update Format",
            value="Post messages containing both 'yesterday' and 'today':\n```Yesterday:\n<what you did>\n\nToday:\n<what you'll do>```\n\nOr simply:\n```Yesterday I fixed bugs, today I'll deploy```",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    # Error handler for slash commands
    @bot.tree.error
    async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
        else:
            print(f"Slash command error: {error}")
            if not interaction.response.is_done():
                await interaction.response.send_message(f"An error occurred: {str(error)}", ephemeral=True)
            else:
                await interaction.followup.send(f"An error occurred: {str(error)}", ephemeral=True)

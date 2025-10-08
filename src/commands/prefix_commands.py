import discord
from discord.ext import commands
import asyncio
import json
import os
from datetime import datetime
from config import TIMEZONE, STANDUP_START_HOUR, STANDUP_START_MINUTE, STANDUP_END_HOUR, STANDUP_END_MINUTE


def register_commands(bot):
    """Register all bot commands"""

    @bot.command(name='test_standup')
    @commands.has_permissions(administrator=True)
    async def test_standup(ctx):
        """Test standup manually (Admin only)"""
        from src.core.utils import start_standup, end_standup

        if not bot.is_standup_active:
            bot.is_standup_active = True

            # Check for async updates first
            await ctx.send("🔍 Checking for async updates...")
            bot.tracker.async_updates_today = await bot.tracker.check_day_highlights()

            # Send status message
            async_count = len(bot.tracker.async_updates_today)
            await ctx.send(
                f"✅ Found {async_count} async update(s)\n"
                f"⏱️ Standup test started! Will end in 30 seconds..."
            )

            await start_standup(bot)

            # Auto-end after 30 seconds for testing
            await asyncio.sleep(30)
            await end_standup(bot)
            bot.is_standup_active = False
        else:
            await ctx.send("⚠️ Standup is already active!")

    @bot.command(name='attendance')
    async def check_attendance(ctx):
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
                await ctx.send(embed=embed)
            else:
                await ctx.send("No one is currently in the standup channel.")
        else:
            await ctx.send("Standup is not currently active.")

    @bot.command(name='async_check')
    async def check_async(ctx):
        """Check today's async updates"""
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

            await ctx.send(embed=embed)
        else:
            await ctx.send("No async updates found for today before cutoff time.")

    @bot.command(name='standup_stats')
    async def standup_stats(ctx, days: int = 7):
        """Get standup statistics for the last N days"""
        # Load attendance records
        current_month = datetime.now(TIMEZONE).strftime("%Y_%m")
        filename = f'data/attendance_{current_month}.json'

        if not os.path.exists(filename):
            await ctx.send("No attendance data available yet.")
            return

        with open(filename, 'r') as f:
            records = json.load(f)

        # Get last N days of records
        recent_records = records[-days:] if len(records) > days else records

        if not recent_records:
            await ctx.send("No records found.")
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

        await ctx.send(embed=embed)

    @bot.command(name='help_standup')
    async def help_standup(ctx):
        """Show help for standup bot commands"""
        embed = discord.Embed(
            title="🤖 Standup Bot Commands",
            description="Here are all available commands:",
            color=discord.Color.green()
        )

        commands_list = [
            ("!attendance", "Check current standup attendance"),
            ("!async_check", "View today's async updates"),
            ("!standup_stats [days]", "Get statistics for last N days (default: 7)"),
            ("!test_standup", "Test standup manually (Admin only)"),
            ("!help_standup", "Show this help message")
        ]

        for cmd, desc in commands_list:
            embed.add_field(name=cmd, value=desc, inline=False)

        embed.add_field(
            name="Schedule",
            value=f"**Daily Standup:** {STANDUP_START_HOUR:02d}:{STANDUP_START_MINUTE:02d} - "
                  f"{STANDUP_END_HOUR:02d}:{STANDUP_END_MINUTE:02d} (Asia/Dhaka)\n"
                  f"**Async Cutoff:** {STANDUP_START_HOUR:02d}:{STANDUP_START_MINUTE:02d}",
            inline=False
        )

        await ctx.send(embed=embed)

    @bot.event
    async def on_command_error(ctx, error):
        """Error handling"""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        elif isinstance(error, commands.CommandNotFound):
            pass  # Ignore unknown commands
        else:
            print(f"Error: {error}")
            await ctx.send(f"An error occurred: {str(error)}")

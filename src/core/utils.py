import discord
import json
import os
from datetime import datetime
from config import TIMEZONE, REPORT_CHANNEL_ID, TEAM_MEMBER_IDS, STANDUP_START_HOUR, STANDUP_START_MINUTE, STANDUP_END_HOUR, STANDUP_END_MINUTE


async def start_standup(bot):
    """Start the standup session"""
    print("\n" + "="*50)
    print("🎯 STARTING DAILY STANDUP")
    print("="*50)

    bot.tracker.start_time = datetime.now(TIMEZONE)
    bot.tracker.attendance.clear()

    # Join voice channel
    await bot.tracker.join_standup_channel()

    # Check async updates
    bot.tracker.async_updates_today = await bot.tracker.check_day_highlights()

    # Initial attendance check
    await bot.tracker.track_attendance()

    # Calculate duration from config
    start_minutes = STANDUP_START_HOUR * 60 + STANDUP_START_MINUTE
    end_minutes = STANDUP_END_HOUR * 60 + STANDUP_END_MINUTE
    duration_minutes = end_minutes - start_minutes
    
    # Send start notification
    report_channel = bot.get_channel(REPORT_CHANNEL_ID)
    if report_channel:
        embed = discord.Embed(
            title="🎯 Daily Standup Started",
            description=f"**Time:** {bot.tracker.start_time.strftime('%I:%M %p')}\n"
                       f"**Duration:** {duration_minutes} minutes\n"
                       f"**Status:** Tracking attendance...",
            color=discord.Color.green(),
            timestamp=bot.tracker.start_time
        )

        # Add async updates preview
        if bot.tracker.async_updates_today:
            async_list = []
            for user_id, data in list(bot.tracker.async_updates_today.items())[:5]:
                async_list.append(f"✅ **{data['name']}** at {data['time']}")

            embed.add_field(
                name=f"📝 Day Highlights Received ({len(bot.tracker.async_updates_today)})",
                value="\n".join(async_list) or "None yet",
                inline=False
            )
        else:
            embed.add_field(
                name="📝 Day Highlights",
                value="No async updates received before cutoff",
                inline=False
            )

        embed.set_footer(text="Standup Bot | Asia/Dhaka")
        await report_channel.send(embed=embed)


async def end_standup(bot):
    """End the standup session and generate report"""
    print("\n" + "="*50)
    print("🏁 ENDING DAILY STANDUP")
    print("="*50)

    bot.tracker.end_time = datetime.now(TIMEZONE)

    # Final attendance check
    await bot.tracker.track_attendance()

    # Leave voice channel
    await bot.tracker.leave_standup_channel()

    # Generate and send report
    await generate_attendance_report(bot)

    # Save records
    await save_attendance_record(bot)


async def generate_attendance_report(bot):
    """Generate comprehensive attendance report"""
    report_channel = bot.get_channel(REPORT_CHANNEL_ID)
    if not report_channel:
        return

    guild = report_channel.guild
    duration = (bot.tracker.end_time - bot.tracker.start_time).total_seconds() / 60

    # Categorize members
    voice_attendees = []
    async_only = []
    no_participation = []

    # Get voice attendees
    for member_id in bot.tracker.attendance:
        member = guild.get_member(member_id)
        if member:
            voice_attendees.append(member.display_name)

    # Get async-only participants
    for member_id, data in bot.tracker.async_updates_today.items():
        if member_id not in bot.tracker.attendance:
            async_only.append(data['name'])

    # Check for team members with no participation (if configured)
    if TEAM_MEMBER_IDS:
        for member_id in TEAM_MEMBER_IDS:
            if (member_id not in bot.tracker.attendance and
                member_id not in bot.tracker.async_updates_today):
                member = guild.get_member(member_id)
                if member:
                    no_participation.append(member.display_name)

    # Create report embed
    embed = discord.Embed(
        title="📊 Daily Standup Report",
        description=f"**Date:** {bot.tracker.end_time.strftime('%B %d, %Y')}\n"
                   f"**Duration:** {duration:.0f} minutes\n"
                   f"**Total Participation:** {len(voice_attendees) + len(async_only)}",
        color=discord.Color.blue(),
        timestamp=bot.tracker.end_time
    )

    # Add attendance fields
    if voice_attendees:
        embed.add_field(
            name=f"🎙️ Voice Attendance ({len(voice_attendees)})",
            value="\n".join(f"• {name}" for name in sorted(voice_attendees))[:1024],
            inline=True
        )

    if async_only:
        embed.add_field(
            name=f"📝 Async Only ({len(async_only)})",
            value="\n".join(f"• {name}" for name in sorted(async_only))[:1024],
            inline=True
        )

    if no_participation:
        embed.add_field(
            name=f"❌ No Participation ({len(no_participation)})",
            value="\n".join(f"• {name}" for name in sorted(no_participation))[:1024],
            inline=True
        )

    # Add summary
    total_team = len(TEAM_MEMBER_IDS) if TEAM_MEMBER_IDS else len(voice_attendees) + len(async_only)
    participation_rate = ((len(voice_attendees) + len(async_only)) / total_team * 100) if total_team > 0 else 0

    embed.add_field(
        name="📈 Statistics",
        value=f"**Participation Rate:** {participation_rate:.1f}%\n"
              f"**Voice Attendees:** {len(voice_attendees)}\n"
              f"**Async Updates:** {len(bot.tracker.async_updates_today)}\n"
              f"**No Shows:** {len(no_participation)}",
        inline=False
    )

    # Add performance indicator
    if participation_rate >= 90:
        embed.color = discord.Color.green()
        status = "🟢 Excellent"
    elif participation_rate >= 70:
        embed.color = discord.Color.yellow()
        status = "🟡 Good"
    else:
        embed.color = discord.Color.red()
        status = "🔴 Needs Improvement"

    embed.set_footer(text=f"Status: {status} | Standup Bot")

    await report_channel.send(embed=embed)


async def save_attendance_record(bot):
    """Save attendance data for historical tracking"""
    today = datetime.now(TIMEZONE).strftime("%Y-%m-%d")

    record = {
        'date': today,
        'day': datetime.now(TIMEZONE).strftime("%A"),
        'start_time': bot.tracker.start_time.isoformat() if bot.tracker.start_time else None,
        'end_time': bot.tracker.end_time.isoformat() if bot.tracker.end_time else None,
        'voice_attendance': list(bot.tracker.attendance),
        'voice_count': len(bot.tracker.attendance),
        'async_updates': {
            str(k): v for k, v in bot.tracker.async_updates_today.items()
        },
        'async_count': len(bot.tracker.async_updates_today),
        'total_participation': len(bot.tracker.attendance) + len([
            uid for uid in bot.tracker.async_updates_today
            if uid not in bot.tracker.attendance
        ])
    }

    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)

    filename = f'data/attendance_{datetime.now(TIMEZONE).strftime("%Y_%m")}.json'

    # Load existing records
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            records = json.load(f)
    else:
        records = []

    records.append(record)

    # Save updated records
    with open(filename, 'w') as f:
        json.dump(records, f, indent=2)

    print(f"💾 Attendance saved to {filename}")

from discord.ext import tasks
from datetime import datetime, time
from config import (
    TIMEZONE,
    STANDUP_START_HOUR,
    STANDUP_START_MINUTE,
    STANDUP_END_HOUR,
    STANDUP_END_MINUTE,
    PRECHECK_HOUR,
    PRECHECK_MINUTE
)


def create_tasks(bot):
    """Create task loops bound to the bot instance"""
    from src.core.utils import start_standup, end_standup

    @tasks.loop(seconds=30)
    async def minute_checker():
        """Check every 30 seconds for standup time"""
        now = datetime.now(TIMEZONE)
        current_time = now.time()

        # Skip weekends (Saturday=5, Sunday=6)
        if now.weekday() >= 5:
            return

        # Check if it's standup start time
        if (current_time.hour == STANDUP_START_HOUR and
            current_time.minute == STANDUP_START_MINUTE and
            current_time.second < 30 and
            not bot.is_standup_active):

            bot.is_standup_active = True
            await start_standup(bot)

        # Track attendance during standup (every 5 minutes)
        elif bot.is_standup_active and current_time.minute % 5 == 0 and current_time.second < 30:
            await bot.tracker.track_attendance()
            print(f"📊 Attendance update: {len(bot.tracker.attendance)} members")

        # Check if it's standup end time
        elif (current_time.hour == STANDUP_END_HOUR and
              current_time.minute == STANDUP_END_MINUTE and
              current_time.second < 30 and
              bot.is_standup_active):

            await end_standup(bot)
            bot.is_standup_active = False

    @tasks.loop(time=time(PRECHECK_HOUR, PRECHECK_MINUTE, tzinfo=TIMEZONE))
    async def standup_scheduler():
        """Pre-standup check for async updates"""
        now = datetime.now(TIMEZONE)

        # Skip weekends
        if now.weekday() >= 5:
            return

        print("🔍 Checking for async updates before standup...")
        bot.tracker.async_updates_today = await bot.tracker.check_day_highlights()
        print(f"📝 Found {len(bot.tracker.async_updates_today)} async updates")

    return minute_checker, standup_scheduler

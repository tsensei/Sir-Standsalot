import discord
from datetime import datetime
import pytz
from config import (
    STANDUP_CHANNEL_ID,
    ASYNC_UPDATE_CHANNEL_ID,
    TIMEZONE,
    ASYNC_CUTOFF_HOUR,
    ASYNC_CUTOFF_MINUTE
)


class StandupTracker:
    def __init__(self, bot):
        self.bot = bot
        self.attendance = set()
        self.async_updates_today = {}
        self.voice_channel = None
        self.start_time = None
        self.end_time = None

    async def join_standup_channel(self):
        """Join the standup voice channel"""
        try:
            channel = self.bot.get_channel(STANDUP_CHANNEL_ID)
            if channel and isinstance(channel, discord.VoiceChannel):
                if not any(vc.channel.id == STANDUP_CHANNEL_ID for vc in self.bot.voice_clients):
                    self.voice_channel = await channel.connect()
                    print(f"🔊 Joined voice channel: {channel.name}")
                    return True
        except Exception as e:
            print(f"❌ Error joining channel: {e}")
        return False

    async def leave_standup_channel(self):
        """Leave the standup voice channel"""
        try:
            for vc in self.bot.voice_clients:
                if vc.channel.id == STANDUP_CHANNEL_ID:
                    await vc.disconnect()
                    print("🔇 Left standup channel")
        except Exception as e:
            print(f"❌ Error leaving channel: {e}")

    async def track_attendance(self):
        """Track who's in the voice channel during standup"""
        channel = self.bot.get_channel(STANDUP_CHANNEL_ID)
        if channel and isinstance(channel, discord.VoiceChannel):
            members_in_vc = []
            for member in channel.members:
                if not member.bot:
                    self.attendance.add(member.id)
                    members_in_vc.append({
                        'id': member.id,
                        'name': member.display_name,
                        'joined_at': datetime.now(TIMEZONE)
                    })
            return members_in_vc
        return []

    async def check_day_highlights(self):
        """Check who sent their day highlights before cutoff"""
        channel = self.bot.get_channel(ASYNC_UPDATE_CHANNEL_ID)
        if not channel:
            print("❌ Async update channel not found")
            return {}

        now = datetime.now(TIMEZONE)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_time = now.replace(hour=ASYNC_CUTOFF_HOUR, minute=ASYNC_CUTOFF_MINUTE, second=0, microsecond=0)

        print(f"🔍 Scanning async updates...")
        print(f"   Current time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print(f"   Today start: {today_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Cutoff time: {cutoff_time.strftime('%Y-%m-%d %H:%M:%S')}")

        async_updates = {}
        messages_checked = 0
        messages_matched = 0

        try:
            async for message in channel.history(after=today_start, limit=100):
                messages_checked += 1
                msg_time = message.created_at.replace(tzinfo=pytz.UTC).astimezone(TIMEZONE)

                # Debug first 3 messages
                if messages_checked <= 3:
                    print(f"   Message {messages_checked}: {message.author.display_name} at {msg_time.strftime('%H:%M')}")
                    print(f"      Content preview: {message.content[:50]}...")

                # Skip if after cutoff time
                if msg_time >= cutoff_time:
                    if messages_checked <= 3:
                        print(f"      ⏰ After cutoff - skipped")
                    continue

                # Skip bots
                if message.author.bot:
                    continue

                # Check if message contains "Yesterday:" and "Today:" pattern
                content_lower = message.content.lower()
                if 'yesterday:' in content_lower and 'today:' in content_lower:
                    if message.author.id not in async_updates:
                        messages_matched += 1
                        async_updates[message.author.id] = {
                            'name': message.author.display_name,
                            'message': message.content[:200],
                            'time': msg_time.strftime("%H:%M")
                        }
                        print(f"   ✅ Found async update from {message.author.display_name}")
                elif messages_checked <= 3:
                    print(f"      ❌ Missing Yesterday/Today keywords")

            print(f"📊 Scanned {messages_checked} messages, found {messages_matched} async updates")

        except Exception as e:
            print(f"❌ Error checking highlights: {e}")
            import traceback
            traceback.print_exc()

        return async_updates

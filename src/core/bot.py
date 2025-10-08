import discord
from discord.ext import commands


class StandupBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.voice_states = True
        intents.members = True
        intents.presences = True

        super().__init__(command_prefix='!', intents=intents)

        self.attendance_data = {}
        self.async_updates = {}
        self.is_standup_active = False
        self.tracker = None  # Will be set after initialization
        self.standup_scheduler = None
        self.minute_checker = None

    async def on_ready(self):
        from config import STANDUP_START_HOUR, STANDUP_START_MINUTE, STANDUP_END_HOUR, STANDUP_END_MINUTE

        print(f'✅ {self.user} has connected to Discord!')
        print(f'📍 Timezone: Asia/Dhaka')
        print(f'⏰ Standup Time: {STANDUP_START_HOUR:02d}:{STANDUP_START_MINUTE:02d} - {STANDUP_END_HOUR:02d}:{STANDUP_END_MINUTE:02d}')

        # Start background tasks
        self.standup_scheduler.start()
        self.minute_checker.start()

    async def setup_hook(self):
        try:
            await self.tree.sync()
            print("✅ Slash commands synced")
        except Exception as e:
            print(f"⚠️ Slash command sync failed: {e}")
            print("Note: Prefix commands (!) will still work")

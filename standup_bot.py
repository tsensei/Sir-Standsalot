import discord
from config import DISCORD_TOKEN
from src.core.bot import StandupBot
from src.core.tracker import StandupTracker
from src.core.tasks import create_tasks
from src.commands.prefix_commands import register_commands
from src.commands.slash_commands import register_slash_commands


def main():
    """Initialize and run the bot"""
    if not DISCORD_TOKEN:
        print("❌ ERROR: Discord token not found in .env file!")
        exit(1)

    # Initialize bot
    bot = StandupBot()

    # Register commands first (before setup_hook runs)
    register_commands(bot)
    register_slash_commands(bot)

    # Initialize tracker
    bot.tracker = StandupTracker(bot)

    # Create and assign tasks bound to bot
    minute_checker, standup_scheduler = create_tasks(bot)
    bot.minute_checker = minute_checker
    bot.standup_scheduler = standup_scheduler

    # Run the bot
    try:
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        print("❌ ERROR: Invalid Discord token!")
    except Exception as e:
        print(f"❌ ERROR: {e}")


if __name__ == "__main__":
    main()

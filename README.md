<div align="center">
  <img src="assets/cover.png" alt="Sir Standsalot Banner" width="100%">

  # Sir Standsalot 🛡️

  *The noble guardian of your daily standup attendance*
</div>

A Discord bot of distinguished service, Sir Standsalot keeps vigilant watch over your team's standup ceremonies. With unwavering dedication, he tracks attendance, honors async updates, and chronicles the daily gatherings of your noble fellowship.

## His Noble Duties

- 🎙️ **Guards the Voice Chamber** - Tracks all who attend the standup assembly
- 📝 **Receives Written Decrees** - Detects async updates in "Yesterday/Today" format
- 📊 **Chronicles the Proceedings** - Generates detailed attendance reports
- 💾 **Maintains the Records** - Preserves historical data for posterity
- ⚙️ **Serves with Flexibility** - Fully configurable via environment variables

## Summoning Sir Standsalot

```bash
# 1. Prepare thy workspace
git clone <repo>
cd discord_attendance_bot
poetry install && poetry add pynacl

# 2. Bestow thy credentials
cp .env.example .env
# Edit .env with your Discord token and channel IDs

# 3. Call him to service
poetry run python standup_bot.py
```

**Via the Docker Vessel:**
```bash
cp .env.example .env
# Edit .env with thy credentials
docker-compose up -d
```

## The Ancient Scrolls (Documentation)

All sacred knowledge resides in the [wiki/](wiki/) halls:

- **[Setup](wiki/Setup.md)** - Summoning Sir Standsalot to your realm
- **[Configuration](wiki/Configuration.md)** - Configuring his noble duties
- **[Commands](wiki/Commands.md)** - Commanding Sir Standsalot's services
- **[Docker](wiki/Docker.md)** - Deploying via the Docker vessel

## Prerequisites for Service

- Python 3.12+ (or Docker vessel)
- A Discord realm with these royal permissions granted:
  - Message Content
  - Server Members
  - Presence

## Oath of Service

*"I, Sir Standsalot, do solemnly swear to faithfully track all standup gatherings, honor every async decree, and maintain accurate records of thy team's noble participation. So help me, Discord."*

## Support & Counsel

- 📖 [Sacred Documentation](wiki/)
- 🐛 [Report Issues](../../issues)
- 💬 [Seek Counsel](../../discussions)

## License

MIT License - Free for all noble causes

---

*Sir Standsalot - Ever vigilant, always counting* 🛡️⚔️

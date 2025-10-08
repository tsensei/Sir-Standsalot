# Setup Guide

Complete guide to setting up the Discord Standup Bot.

## Prerequisites

- Discord account with server admin access
- Python 3.12+ and Poetry (or Docker)

## Step 1: Create Discord Bot

### 1.1 Create Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application**
3. Name it (e.g., "Standup Bot")
4. Click **Create**

### 1.2 Enable Intents

1. Go to **Bot** section (left sidebar)
2. Scroll to **Privileged Gateway Intents**
3. Enable these three:
   - ✅ **Presence Intent**
   - ✅ **Server Members Intent**
   - ✅ **Message Content Intent**
4. Click **Save Changes**

### 1.3 Get Bot Token

1. In the **Bot** section
2. Click **Reset Token**
3. Copy the token (save it securely)

### 1.4 Invite Bot to Server

1. Go to **OAuth2** → **URL Generator**
2. Select **Scopes:**
   - `bot`
   - `applications.commands`
3. Select **Bot Permissions:**
   - Read Messages/View Channels
   - Send Messages
   - Embed Links
   - Read Message History
   - Connect (Voice)
   - Speak (Voice)
   - Use Slash Commands
4. Copy the generated URL
5. Open URL in browser and invite to your server

## Step 2: Get Channel IDs

### 2.1 Enable Developer Mode

1. Discord **Settings** → **Advanced**
2. Enable **Developer Mode**

### 2.2 Copy Channel IDs

Right-click each channel → **Copy Channel ID**

You need IDs for:
- **Voice channel** - Where standup happens
- **Text channel** - Where team posts async updates
- **Text channel** - Where bot posts reports (can be same as updates)

## Step 3: Configure Environment

### 3.1 Create .env File

```bash
cp .env.example .env
```

### 3.2 Edit Required Variables

```env
DISCORD_TOKEN=your_bot_token_here
STANDUP_VOICE_CHANNEL_ID=123456789012345678
ASYNC_UPDATE_CHANNEL_ID=123456789012345678
REPORT_CHANNEL_ID=123456789012345678
```

That's all that's required! See [Configuration](Configuration.md) for optional settings.

## Step 4: Install and Run

### Option A: Python

```bash
# Install dependencies
poetry install
poetry add pynacl  # Required for voice

# Run
poetry run python standup_bot.py
```

### Option B: Docker

```bash
# Run
docker-compose up -d

# View logs
docker-compose logs -f
```

## Step 5: Verify

1. Bot should appear online in Discord
2. Type `/help` in any channel
3. You should see slash commands appear

Test with `/test_standup` (admin only) to run a quick test.

## Next Steps

- **Customize schedule:** Edit `.env` - see [Configuration](Configuration.md)
- **Deploy to production:** See [Docker](Docker.md)
- **Learn commands:** See [Commands](Commands.md)

## Troubleshooting

### Bot appears offline
- Check `DISCORD_TOKEN` is correct
- Verify token hasn't been regenerated

### Bot doesn't respond to commands
- Ensure **Message Content Intent** is enabled
- Check bot has permission in the channel

### Can't join voice channel
```bash
poetry add pynacl
```

### Channel not found errors
- Verify channel IDs are correct
- Ensure bot has access to those channels

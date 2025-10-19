# Configuration Reference

Complete environment variable reference.

## Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DISCORD_TOKEN` | Bot authentication token | `MTQyNTM2...` |
| `STANDUP_VOICE_CHANNEL_ID` | Voice channel for standup | `1313914957959532585` |
| `ASYNC_UPDATE_CHANNEL_ID` | Text channel for async updates | `1384945767181189162` |
| `REPORT_CHANNEL_ID` | Text channel for reports | `1425363894544891975` |

## Optional Variables

### Schedule Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `TIMEZONE` | String | `Asia/Dhaka` | IANA timezone identifier |
| `STANDUP_START_HOUR` | 0-23 | `11` | Standup start hour |
| `STANDUP_START_MINUTE` | 0-59 | `0` | Standup start minute |
| `STANDUP_END_HOUR` | 0-23 | `11` | Standup end hour |
| `STANDUP_END_MINUTE` | 0-59 | `15` | Standup end minute |
| `ASYNC_CUTOFF_HOUR` | 0-23 | Same as start | Async deadline hour |
| `ASYNC_CUTOFF_MINUTE` | 0-59 | Same as start | Async deadline minute |
| `PRECHECK_HOUR` | 0-23 | `10` | Pre-check hour |
| `PRECHECK_MINUTE` | 0-59 | `55` | Pre-check minute |

### Team Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `TEAM_MEMBER_IDS` | CSV | Empty | Discord user IDs (comma-separated) |

### Email Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `FROM_EMAIL` | String | None | Sender email address |
| `TO_EMAILS` | CSV | Empty | Recipient emails (comma-separated) |
| `RESEND_API_KEY` | String | None | Resend API key for sending emails |

## Getting Values

### Discord Token
1. [Discord Developer Portal](https://discord.com/developers/applications)
2. Your App → Bot → Reset Token

### Channel IDs
1. Discord Settings → Advanced → Enable Developer Mode
2. Right-click channel → Copy Channel ID

### User IDs
1. Right-click user → Copy User ID
2. Format: `123456,234567,345678` (comma-separated)

### Email Setup
1. [Resend Account](https://resend.com) - Sign up for free
2. Get API key from dashboard
3. Verify your domain (or use Resend's test domain)
4. Format: `noreply@yourcompany.com,manager@company.com`

## Common Timezones

| Region | Timezone |
|--------|----------|
| US East | `America/New_York` |
| US West | `America/Los_Angeles` |
| US Central | `America/Chicago` |
| UK | `Europe/London` |
| India | `Asia/Kolkata` |
| Singapore | `Asia/Singapore` |
| Japan | `Asia/Tokyo` |
| Australia | `Australia/Sydney` |

[Full list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

## Understanding Timing

### Default Schedule
```
10:55 AM - Bot checks for async updates
11:00 AM - Standup starts, bot joins voice
11:15 AM - Standup ends, report generated
```

### Async Cutoff Time

**Purpose:** Deadline for async updates to count.

**Example 1: Same as standup start (default)**
```env
STANDUP_START_HOUR=11
ASYNC_CUTOFF_HOUR=11  # Posts before 11:00 count
```

**Example 2: Earlier deadline**
```env
STANDUP_START_HOUR=11
ASYNC_CUTOFF_HOUR=10  # Posts before 10:00 count
```
Posts between 10:00-11:00 won't count.

### Pre-check Time

**Purpose:** When bot scans for async updates before standup.

```env
PRECHECK_HOUR=10
PRECHECK_MINUTE=55    # Scan at 10:55
STANDUP_START_HOUR=11 # Standup at 11:00
```

**Recommendation:** Set 5-10 minutes before standup.

## Example Configurations

### Minimal (Defaults)
```env
DISCORD_TOKEN=your_token
STANDUP_VOICE_CHANNEL_ID=123456789012345678
ASYNC_UPDATE_CHANNEL_ID=123456789012345678
REPORT_CHANNEL_ID=123456789012345678
```

### US Team
```env
DISCORD_TOKEN=your_token
STANDUP_VOICE_CHANNEL_ID=123456789012345678
ASYNC_UPDATE_CHANNEL_ID=123456789012345678
REPORT_CHANNEL_ID=123456789012345678
TIMEZONE=America/New_York
STANDUP_START_HOUR=9
STANDUP_START_MINUTE=30
STANDUP_END_HOUR=9
STANDUP_END_MINUTE=45
```

### Strict Async Policy
```env
DISCORD_TOKEN=your_token
STANDUP_VOICE_CHANNEL_ID=123456789012345678
ASYNC_UPDATE_CHANNEL_ID=123456789012345678
REPORT_CHANNEL_ID=123456789012345678
TIMEZONE=Europe/London
STANDUP_START_HOUR=10
STANDUP_END_MINUTE=15
ASYNC_CUTOFF_HOUR=9        # Due 1 hour before
PRECHECK_HOUR=9
PRECHECK_MINUTE=55
TEAM_MEMBER_IDS=111,222,333
```

### With Email Summaries
```env
DISCORD_TOKEN=your_token
STANDUP_VOICE_CHANNEL_ID=123456789012345678
ASYNC_UPDATE_CHANNEL_ID=123456789012345678
REPORT_CHANNEL_ID=123456789012345678
TIMEZONE=America/New_York
STANDUP_START_HOUR=9
STANDUP_START_MINUTE=30
STANDUP_END_HOUR=9
STANDUP_END_MINUTE=45
FROM_EMAIL=noreply@yourcompany.com
TO_EMAILS=manager@yourcompany.com,team@yourcompany.com,stakeholder@yourcompany.com
RESEND_API_KEY=re_xxxxxxxxxx
```

## Validation

### Missing Required Variables
```
❌ ERROR: Discord token not found in .env file!
```

### Invalid Timezone
```
UnknownTimeZoneError: 'Invalid/Timezone'
```

### Invalid Channel ID
```
❌ Async update channel not found
```

Check bot has permission to view the channel.

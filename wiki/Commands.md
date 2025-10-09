# Bot Commands

All available commands and their usage.

## Slash Commands

Type `/` in Discord to see autocomplete.

### `/help`
Shows all available commands and bot information.

### `/attendance`
Check who's currently in the standup voice channel.

**When to use:** During an active standup.

**Example output:**
```
📊 Current Attendance
In Voice Channel: 5

• Alice
• Bob
• Charlie
• David
• Eve
```

### `/async_check`
View who posted async updates today before the cutoff time.

**Example output:**
```
📝 Today's Async Updates
Found 3 updates before cutoff

Alice at 10:30
Yesterday: Fixed bug #123
Today: Will work on feature X

Bob at 10:45
Yesterday: Code review
Today: Testing deployment
```

### `/standup_stats [days]`
Get attendance statistics for the last N days (default: 7).

**Usage:**
- `/standup_stats` - Last 7 days
- `/standup_stats 30` - Last 30 days

**Example output:**
```
📈 Standup Statistics (Last 7 days)

Summary
Total Voice Attendance: 35
Total Async Updates: 21
Avg. Participation: 8.0

Recent Days
2025-10-08: 🎙️ 5 | 📝 3
2025-10-07: 🎙️ 4 | 📝 4
2025-10-06: 🎙️ 6 | 📝 2
```

### `/test_standup` (Admin only)
Manually trigger a test standup (lasts 30 seconds).

**Usage:** Test bot configuration without waiting for scheduled time.

**What it does:**
1. Checks for async updates in the channel
2. Shows how many async updates were found
3. Runs a 30-second standup
4. Generates a report at the end

**Example output:**
```
🔍 Checking for async updates...
✅ Found 3 async update(s)
⏱️ Standup test started! Will end in 30 seconds...

[30 seconds later, in report channel]
📊 Daily Standup Report
...
```

**Testing tip:** Post a message with "Yesterday:" and "Today:" in the async channel before running this command to test async update detection.

## Prefix Commands

If slash commands aren't working, use prefix commands with `!`:

- `!help_standup` - Same as `/help`
- `!attendance` - Same as `/attendance`
- `!async_check` - Same as `/async_check`
- `!standup_stats [days]` - Same as `/standup_stats`
- `!test_standup` - Same as `/test_standup`

## Async Update Format

For messages to be detected as async updates, they must contain **both** keywords:

```
Yesterday:
- What you accomplished
- Tasks completed

Today:
- What you'll work on
- Goals for today
```

**Valid formats:**
```
Yesterday:
Fixed login bug

Today:
Will deploy to production
```

```
Yesterday: Code review
Today: Write tests
```

```
Yesterday I fixed the bug, today I'll deploy
```

```
Completed task A yesterday, will do task B today
```

**Invalid formats:**
```
Today:
Will work on feature X
(Missing "yesterday" keyword)
```

```
Will work on feature X
(Missing both "yesterday" and "today" keywords)
```

## Report Format

After each standup, bot posts a report:

```
📊 Daily Standup Report
Date: October 8, 2025
Duration: 15 minutes
Total Participation: 8

🎙️ Voice Attendance (5)
• Alice
• Bob
• Charlie
• David
• Eve

📝 Async Only (3)
• Frank
• Grace
• Henry

❌ No Participation (2)
• Ian
• Jane

📈 Statistics
Participation Rate: 80.0%
Voice Attendees: 5
Async Updates: 8
No Shows: 2

Status: 🟢 Excellent | Standup Bot
```

### Participation Categories

- **🎙️ Voice Attendance** - Joined voice channel during standup
- **📝 Async Only** - Posted update but didn't join voice
- **❌ No Participation** - Neither (only shown if TEAM_MEMBER_IDS is set)

### Status Indicators

- 🟢 **Excellent** - 90%+ participation
- 🟡 **Good** - 70-89% participation
- 🔴 **Needs Improvement** - <70% participation

## Permissions

### Regular Users
- Can use all view commands: `/help`, `/attendance`, `/async_check`, `/standup_stats`
- Can post async updates

### Administrators
- Can use `/test_standup`
- Same access as regular users

## Troubleshooting

### Commands don't appear
- Slash commands may take a few minutes to sync after bot starts
- Try restarting Discord client
- Fall back to prefix commands (`!command`)

### "/help doesn't show my commands"
- Bot needs `Use Application Commands` permission
- Check bot role permissions in server settings

### "You don't have permission to use this command"
- `/test_standup` requires Administrator permission
- Check your role has Admin permission

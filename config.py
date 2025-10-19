import os
from dotenv import load_dotenv
import pytz

# Load environment variables
load_dotenv()

# Discord Configuration (Required)
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
STANDUP_CHANNEL_ID = int(os.getenv('STANDUP_VOICE_CHANNEL_ID'))
ASYNC_UPDATE_CHANNEL_ID = int(os.getenv('ASYNC_UPDATE_CHANNEL_ID'))
REPORT_CHANNEL_ID = int(os.getenv('REPORT_CHANNEL_ID'))

# Timezone Configuration
TIMEZONE = pytz.timezone(os.getenv('TIMEZONE', 'Asia/Dhaka'))

# Standup Times (24-hour format)
STANDUP_START_HOUR = int(os.getenv('STANDUP_START_HOUR', '11'))
STANDUP_START_MINUTE = int(os.getenv('STANDUP_START_MINUTE', '0'))
STANDUP_END_HOUR = int(os.getenv('STANDUP_END_HOUR', '11'))
STANDUP_END_MINUTE = int(os.getenv('STANDUP_END_MINUTE', '15'))

# Async Update Cutoff Time (when to stop checking for async updates)
# Default is standup start time, but can be set independently
ASYNC_CUTOFF_HOUR = int(os.getenv('ASYNC_CUTOFF_HOUR', str(STANDUP_START_HOUR)))
ASYNC_CUTOFF_MINUTE = int(os.getenv('ASYNC_CUTOFF_MINUTE', str(STANDUP_START_MINUTE)))

# Pre-standup Check Time (when to check async updates before standup)
PRECHECK_HOUR = int(os.getenv('PRECHECK_HOUR', '10'))
PRECHECK_MINUTE = int(os.getenv('PRECHECK_MINUTE', '55'))

# Team Members (Optional - for tracking absent members)
# Set via environment variable TEAM_MEMBER_IDS (comma-separated)
# Example: TEAM_MEMBER_IDS=123456789012345678,234567890123456789
_team_ids_env = os.getenv('TEAM_MEMBER_IDS', '')
if _team_ids_env:
    # Parse from environment (comma-separated list)
    TEAM_MEMBER_IDS = [int(id.strip()) for id in _team_ids_env.split(',') if id.strip()]
else:
    # Empty list if not configured - bot will still work but won't track absences
    TEAM_MEMBER_IDS = []
    print("⚠️  TEAM_MEMBER_IDS not set - absence tracking disabled")

# Email Configuration (Required for email summaries)
FROM_EMAIL = os.getenv('FROM_EMAIL')
TO_EMAILS = os.getenv('TO_EMAILS', '')  # Comma-separated list of email addresses
RESEND_API_KEY = os.getenv('RESEND_API_KEY')

# Parse TO_EMAILS into a list
if TO_EMAILS:
    TO_EMAILS_LIST = [email.strip() for email in TO_EMAILS.split(',') if email.strip()]
else:
    TO_EMAILS_LIST = []
    print("⚠️  TO_EMAILS not set - email summaries disabled")

# Validate email configuration
if not FROM_EMAIL:
    print("⚠️  FROM_EMAIL not set - email summaries disabled")
if not RESEND_API_KEY:
    print("⚠️  RESEND_API_KEY not set - email summaries disabled")
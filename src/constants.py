"""
Constants and string templates used throughout the application
"""

# Bot Messages
WELCOME_MESSAGE = (
    "*Netflix Code Fetcher Bot*\n\n"
    "I will fetch the link for your Netflix verification code from email\\.\n\n"
    "*Commands:*\n"
    "/netflix\\_code \\- Get the latest Netflix verification code\n"
    "/netflix\\_help \\- Show this help message\n\n"
    "*Note:* Request your Netflix code first, then use /netflix\\_code to fetch it\\!"
).strip()

HELP_MESSAGE = (
    "*Netflix Code Fetcher Bot Help*\n\n"
    "*Available Commands:*\n"
    "/netflix\\_code \\- Fetch the latest Netflix verification code\n"
    "/netflix\\_start \\- Show welcome message\n"
    "/netflix\\_help \\- Show this help\n\n"
    "*How it works:*\n"
    "1\\. Request a verification code from Netflix\n"
    "2\\. Use /netflix\\_code command\n"
    "3\\. I'll fetch your verification code\n\n"
    "*Note:* Make sure to request a new code before using /netflix\\_code"
).strip()

VERIFICATION_LINK_MESSAGE = (
    "*Netflix Verification Link*\n\n"
    "Requested by: {name}\n"
    "Date: {date}\n\n"
    "{link}\n\n"
    "_This link will expire in 15 minutes\\._"
)

ERROR_NO_VERIFICATION_LINK = "*Error*: Could not find verification link in the email\\. Please request a new code\\."
ERROR_EMAIL_FETCH = "*Error*: Could not fetch email\\. Please try again later\\."
ERROR_NO_NETFLIX_EMAILS = "No Netflix verification code emails found"
ERROR_CONFIG_TOKEN = "Please configure telegram.bot.token in config.properties"
ERROR_CONFIG_EMAIL = "Please configure email.address and email.password in config.properties"
ERROR_UNAUTHORIZED = "*Error*: You are not authorized to use this bot."

# Email Configuration
NETFLIX_EMAIL_SENDER = "info@account.netflix.com"
NETFLIX_EMAIL_SUBJECT = "Your Netflix temporary access code"

# Log Messages
LOG_CONFIG_LOADED = "Configuration loaded successfully"
LOG_BOT_STARTING = "Starting Telegram Email Bot..."
LOG_FETCHING_EMAIL = "Fetching Netflix verification code for user {} in chat {}"
LOG_BOT_STOPPED = "Bot stopped by user"
LOG_BOT_ERROR = "Bot error: {}"

# Regex Patterns
NETFLIX_LINK_PATTERN = r'https://www\.netflix\.com/account/travel/verify\?[^\s\]]+'
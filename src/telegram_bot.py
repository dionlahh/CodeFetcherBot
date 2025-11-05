"""
Telegram bot implementation for fetching Netflix verification codes
"""

import logging
import urllib.parse
import re
from datetime import datetime
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo
from functools import wraps
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode

from .constants import (
    WELCOME_MESSAGE, HELP_MESSAGE, VERIFICATION_LINK_MESSAGE,
    ERROR_NO_VERIFICATION_LINK, ERROR_EMAIL_FETCH, ERROR_UNAUTHORIZED,
    NETFLIX_LINK_PATTERN, LOG_BOT_STARTING, LOG_FETCHING_EMAIL
)

logger = logging.getLogger(__name__)

def check_authorized(func):
    """Decorator to check if user is authorized"""
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.effective_chat.id not in self.authorized_chats:
            logger.warning(f"Unauthorized access attempt from chat ID: {update.effective_chat.id}")
            await update.message.reply_text(
                ERROR_UNAUTHORIZED,
                parse_mode=ParseMode.MARKDOWN_V2
            )
            return
        return await func(self, update, context, *args, **kwargs)
    return wrapper

class TelegramEmailBot:
    """Main Telegram bot class"""
    
    def __init__(self, bot_token: str, email_fetcher, config):
        """Initialize the bot with token and email fetcher"""
        self.bot_token = bot_token
        self.email_fetcher = email_fetcher
        self.application = None
        
        # Get authorized chat IDs
        chat_ids = config.get_list('telegram.authorized_chat_ids', [])
        logger.info(f"Raw authorized chat IDs from config: {chat_ids}")
        
        self.authorized_chats = set()
        for chat_id in chat_ids:
            chat_id = chat_id.strip()
            # Handle negative chat IDs
            if chat_id.startswith('-') and chat_id[1:].isdigit():
                self.authorized_chats.add(int(chat_id))
            elif chat_id.isdigit():
                self.authorized_chats.add(int(chat_id))
                
        logger.info(f"Processed authorized chat IDs: {self.authorized_chats}")
    
    @check_authorized
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /netflix_start command"""
        await update.message.reply_text(
            WELCOME_MESSAGE,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    @check_authorized
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /netflix_help command"""
        await update.message.reply_text(
            HELP_MESSAGE,
            parse_mode=ParseMode.MARKDOWN_V2
        )
    
    @check_authorized
    async def get_code_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /netflix_code command - fetch latest email"""
        try:
            # Send "typing" action to show bot is working
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id, 
                action="typing"
            )
            
            # Fetch latest email
            logger.info(LOG_FETCHING_EMAIL.format(
                update.effective_user.username,
                update.effective_chat.id
            ))
            
            email_data = self.email_fetcher.fetch_latest_email()
            
            if not email_data:
                await update.message.reply_text(
                    ERROR_EMAIL_FETCH,
                    parse_mode=ParseMode.MARKDOWN_V2
                )
                return
            
            # Format the email content for Telegram
            formatted_message = self._format_email_message(email_data)
            
            # Send the email content
            await update.message.reply_text(
                formatted_message,
                parse_mode=ParseMode.MARKDOWN_V2
            )
            
        except Exception as e:
            logger.error(f"Error in get_code_command: {str(e)}")
            await update.message.reply_text(
                ERROR_EMAIL_FETCH,
                parse_mode=ParseMode.MARKDOWN_V2
            )
    
    def _format_email_message(self, email_data: dict) -> str:
        """Format email data for Telegram message, extracting Netflix verification link"""
        body = email_data.get("body", "")
        date_str = email_data.get("date", "")
        
        # Try to extract the verification link from the email body
        link_match = re.search(NETFLIX_LINK_PATTERN, body)
        link = link_match.group(0) if link_match else None
        
        if not link:
            return ERROR_NO_VERIFICATION_LINK
            
        # Try to extract the name
        name_match = re.search(r'Hi ([^,\n]+)', body)
        name = name_match.group(1) if name_match else "Unknown"
            
        # Clean up the link by removing any URL encoding
        clean_link = urllib.parse.unquote(link.replace('=3D', '='))
        
        # Format the date in SGT
        try:
            # Parse the email date string to datetime
            utc_dt = parsedate_to_datetime(date_str)
            # Convert to SGT
            sgt_dt = utc_dt.astimezone(ZoneInfo("Asia/Singapore"))
            # Format date nicely with day of week
            formatted_date = sgt_dt.strftime("%A, %d %B %Y, %I:%M %p SGT")
            # Escape special characters for Markdown V2
            formatted_date = formatted_date.replace('-', '\\-').replace('.', '\\.')
        except Exception:
            formatted_date = "Unknown"
            
        # Escape special characters in name for Markdown V2
        name = name.replace('-', '\\-').replace('.', '\\.').replace('_', '\\_')
        
        return VERIFICATION_LINK_MESSAGE.format(
            name=name,
            date=formatted_date,
            link=f"[Click here to verify]({clean_link})"
        )
    
    def setup_handlers(self):
        """Set up command handlers"""
        self.application.add_handler(CommandHandler("netflix_start", self.start_command))
        self.application.add_handler(CommandHandler("netflix_help", self.help_command))
        self.application.add_handler(CommandHandler("netflix_code", self.get_code_command))
        # Keep old command for backward compatibility
        self.application.add_handler(CommandHandler("getCode", self.get_code_command))
    
    async def run(self):
        """Run the bot"""
        logger.info(LOG_BOT_STARTING)
        await self.application.run_polling()
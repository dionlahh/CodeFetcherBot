#!/usr/bin/env python3
"""
Main entry point for the Netflix Code Fetcher Bot
"""

import logging
from telegram.ext import Application
from src.config import ConfigManager
from src.email_fetcher import EmailFetcher
from src.telegram_bot import TelegramEmailBot
from src.constants import (
    LOG_CONFIG_LOADED,
    ERROR_CONFIG_TOKEN,
    ERROR_CONFIG_EMAIL,
    LOG_BOT_STARTING,
    LOG_BOT_STOPPED,
    LOG_BOT_ERROR,
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load configuration
config = ConfigManager()

def main():
    """Main function to run the bot"""
    try:
        # Get configuration values
        telegram_bot_token = config.get('telegram.bot.token')
        email_server = config.get('email.server')
        email_port = config.get_int('email.port')
        email_address = config.get('email.address')
        email_password = config.get('email.password')
        
        # Print all config values for debugging
        logger.info("Loaded configuration values:")
        logger.info(f"Bot token: {telegram_bot_token}")
        logger.info(f"Authorized chat IDs: {config.get('telegram.authorized_chat_ids')}")
        
        # Validate configuration
        if not telegram_bot_token or telegram_bot_token == "YOUR_BOT_TOKEN_HERE":
            logger.error(ERROR_CONFIG_TOKEN)
            return
        
        if not email_address or not email_password:
            logger.error(ERROR_CONFIG_EMAIL)
            return
        
        # Create email fetcher
        email_fetcher = EmailFetcher(
            server=email_server,
            port=email_port,
            email_addr=email_address,
            password=email_password
        )
        
        # Create bot and application
        bot = TelegramEmailBot(telegram_bot_token, email_fetcher, config)
        bot.application = Application.builder().token(telegram_bot_token).build()
        bot.setup_handlers()
        
        # Start the bot
        bot.application.run_polling()
        
    except KeyboardInterrupt:
        logger.info(LOG_BOT_STOPPED)
    except Exception as e:
        logger.error(LOG_BOT_ERROR.format(str(e)))
        raise

if __name__ == "__main__":
    main()
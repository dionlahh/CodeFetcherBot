"""
Configuration manager for handling application settings
"""

import os
import configparser
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages configuration from properties file"""
    
    def __init__(self, config_file='config.properties'):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        """Load configuration from properties file and environment variables"""
        config_data = '[DEFAULT]\n'
        
        # Try to load from file first
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config_data = '[DEFAULT]\n' + f.read()
                self.config.read_string(config_data)
                logger.info("Configuration loaded from file successfully")
            except Exception as e:
                logger.warning(f"Error loading configuration file: {str(e)}")
        
        # Map environment variables to config keys
        env_mapping = {
            'TELEGRAM_BOT_TOKEN': 'telegram.bot.token',
            'TELEGRAM_AUTHORIZED_CHAT_IDS': 'telegram.authorized_chat_ids',
            'EMAIL_SERVER': 'email.server',
            'EMAIL_PORT': 'email.port',
            'EMAIL_USE_SSL': 'email.use_ssl',
            'EMAIL_ADDRESS': 'email.address',
            'EMAIL_PASSWORD': 'email.password',
            'EMAIL_MAX_BODY_LENGTH': 'email.max_body_length',
            'EMAIL_FETCH_TIMEOUT': 'email.fetch_timeout',
            'LOG_LEVEL': 'log.level'
        }
        
        # Override with environment variables if they exist
        for env_var, config_key in env_mapping.items():
            if os.environ.get(env_var):
                self.config.set('DEFAULT', config_key, os.environ.get(env_var))
                logger.info(f"Configuration overridden by environment variable: {config_key}")
        
        # Verify required configurations
        required_keys = [
            'telegram.bot.token',
            'telegram.authorized_chat_ids',
            'email.server',
            'email.port',
            'email.address',
            'email.password'
        ]
        
        missing_keys = [key for key in required_keys if not self.config.get('DEFAULT', key, fallback=None)]
        if missing_keys:
            raise ValueError(f"Missing required configuration keys: {', '.join(missing_keys)}")
    
    def get(self, key, default=None):
        """Get configuration value"""
        try:
            return self.config.get('DEFAULT', key)
        except (configparser.NoOptionError, configparser.NoSectionError):
            if default is not None:
                return default
            logger.error(f"Configuration key '{key}' not found")
            raise KeyError(f"Configuration key '{key}' not found")
    
    def get_int(self, key, default=None):
        """Get configuration value as integer"""
        value = self.get(key, default)
        return int(value) if value is not None else None
    
    def get_bool(self, key, default=None):
        """Get configuration value as boolean"""
        value = self.get(key, default)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')
        
    def get_list(self, key, default=None):
        """Get configuration value as a list (comma-separated)"""
        value = self.get(key, default)
        if value is None:
            return default if default is not None else []
        return [item.strip() for item in value.split(',') if item.strip()]
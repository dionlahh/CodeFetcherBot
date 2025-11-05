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
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """Load configuration from properties file"""
        if not os.path.exists(self.config_file):
            logger.error(f"Configuration file {self.config_file} not found!")
            raise FileNotFoundError(f"Configuration file {self.config_file} not found!")
        
        try:
            # ConfigParser expects sections, so we'll add a default section
            with open(self.config_file, 'r') as f:
                config_string = '[DEFAULT]\n' + f.read()
            
            self.config.read_string(config_string)
            logger.info("Configuration loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise
    
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
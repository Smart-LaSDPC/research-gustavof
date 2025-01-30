import os
from dotenv import load_dotenv
import streamlit as st

def singleton(cls):
    """Decorator to create singleton classes"""
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Config:
    """Configuration object for environment variables"""
    
    def __init__(self):
        load_dotenv()
        # Define class attributes with default values
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.PROMETHEUS_URL = os.getenv('PROMETHEUS_OPERATOR_URL', 'http://localhost:9090/api/v1/query_range')
        self.MICRO_K8S = os.getenv('MICRO_K8S', 'False').lower() == 'true'
        self.ENVIRONMENT = os.getenv('ENVIRONMENT', 'LOCAL')
        
        # Validate required environment variables
        self._validate_config()
    
    def _validate_config(self):
        """Validate required configuration values"""
        if not self.OPENAI_API_KEY:
            st.error("OpenAI API Key is not set. Please set the `OPENAI_API_KEY` environment variable.")
            st.stop()
    
    def get(self, key, default=None):
        """Get configuration value by key with optional default"""
        return getattr(self, key.upper(), default)

# Create a singleton instance
config = Config()



# Usage example:
# from src.config import config
# api_key = config.OPENAI_API_KEY
# prometheus_url = config.PROMETHEUS_URL
# or
# prometheus_url = config.get('prometheus_url', 'default_url')

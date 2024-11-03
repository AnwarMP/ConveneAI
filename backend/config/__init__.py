import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    # LLM Configuration
    DEFAULT_LLM_PROVIDER = "openai"  # or "anthropic"
    
    # OpenAI specific settings
    OPENAI_MODEL = "gpt-4o-mini"  # GPT-4 Turbo is faster than GPT-4
    OPENAI_TEMPERATURE = 0.1
    
    # Anthropic specific settings
    ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


    # Email Configuration
    # Add to Config class:
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_CREDENTIALS_FILE = 'credentials.json'
    GOOGLE_TOKEN_FILE = 'token.json'
import os
from termcolor import colored
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys and Configuration
try:
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # WhatsApp Configuration
    WHATSAPP_ID_INSTANCE = os.getenv("WHATSAPP_ID_INSTANCE")
    WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
    WHATSAPP_RECIPIENT = os.getenv("WHATSAPP_RECIPIENT")
    
    # YouTube Configuration
    CHANNEL_ID = os.getenv("CHANNEL_ID")

    # Validate required environment variables
    required_vars = {
        "GEMINI_API_KEY": GEMINI_API_KEY,
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "WHATSAPP_ID_INSTANCE": WHATSAPP_ID_INSTANCE,
        "WHATSAPP_API_TOKEN": WHATSAPP_API_TOKEN,
        "WHATSAPP_RECIPIENT": WHATSAPP_RECIPIENT,
        "CHANNEL_ID": CHANNEL_ID
    }

    for var_name, var_value in required_vars.items():
        if not var_value:
            raise ValueError(f"Missing required environment variable: {var_name}")

    print(colored("✓ Environment variables loaded successfully", "green"))

except Exception as e:
    print(colored(f"Error loading configuration: {str(e)}", "red"))
    raise

# Export all variables
__all__ = [
    'GEMINI_API_KEY',
    'OPENAI_API_KEY',
    'WHATSAPP_ID_INSTANCE',
    'WHATSAPP_API_TOKEN',
    'WHATSAPP_RECIPIENT',
    'CHANNEL_ID'
] 
import os
from dotenv import load_dotenv

# Load environment variables from a .env file into os.environ
load_dotenv()

class Config:
    """
    Centralized application configuration loaded from environment variables.
    Adjust values via your .env file or deployment environment.
    """

    # Flask runtime mode: "production" or "development"
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    
    # Enable Flask’s debugger when FLASK_DEBUG="True"
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    # Host and port for app.run(); defaults to 0.0.0.0:5000
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))

    # Maximum characters allowed per outgoing WhatsApp message
    MAX_MSG_CHARS = int(os.getenv("MAX_SMS_CHARS", 1600))

    # Twilio credentials
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    # Twilio Auth Token for request validation
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    # The WhatsApp‑enabled Twilio number you send messages from
    TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
    # Your Twilio webhook URL for incoming messages
    TWILIO_WEBHOOK_URL = os.getenv("TWILIO_WEBHOOK_URL")

    # OpenAI API key for AI processing
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # OpenAI model to use for AI responses
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
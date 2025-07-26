import threading
from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse

from app.settings.config import Config
from app.utils.twilio_validator import validate_twilio_request
from app.services.message_processor import process_incoming
from app.services.twilio_client import send_whatsapp_message
from app.utils.logger import get_logger

bp = Blueprint("whatsapp", __name__)
logger = get_logger(__name__)

# Centralized response messages to avoid duplication
RESPONSE_MESSAGES = {
    "analyzing": "Thanks! I'm analyzing your nutrition label... ⏳",
    "request_image": "Please send me a photo of a nutrition label and I'll analyze it for you! 📸",
    "processing_error": "Sorry, I encountered an error processing your message. Please try again."
}

@bp.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    validate_twilio_request()

    incoming = request.values.get("Body", "").strip()
    sender = request.values.get("From")
    media_url = request.form.get('MediaUrl0')
    phone_number = sender.replace("whatsapp:", "") if sender else ""
    
    logger.info(f"📥 Received from {phone_number} - Text: {incoming[:100]}{'...' if len(incoming) > 100 else ''}")
    if media_url:
        logger.info(f"📥 Media URL: {media_url}")

    def background_task(phone: str, text: str, media_url: str = None):
        """Background processing of the incoming message with memory-efficient streaming."""
        
        try:
            # Use Config class for Twilio credentials
            twilio_account_sid = Config.TWILIO_ACCOUNT_SID
            twilio_auth_token = Config.TWILIO_AUTH_TOKEN
            
            # Use memory-efficient streaming for media processing
            result = process_incoming(
                phone_number=phone,
                text=text,
                media_url=media_url,
                twilio_account_sid=twilio_account_sid,
                twilio_auth_token=twilio_auth_token
            )
        
            if result.get("success"):
                reply = result.get("aiResponse", "Sorry, I couldn't process your message.")
            else:
                reply = result.get("aiResponse", "Sorry, something went wrong. Please try again.")
        
            # Send reply back to user
            send_whatsapp_message(to=sender, body=reply)
            logger.info(f"✅ Sent analysis reply to {phone}: {len(reply)} chars")
        
        except Exception as e:
            logger.error(f"❌ Error in background task for {phone}: {e}")
            # Send error message to user
            try:
                send_whatsapp_message(to=sender, body=RESPONSE_MESSAGES["processing_error"])
            except Exception as send_error:
                logger.error(f"❌ Failed to send error message: {send_error}")

    # Immediate response for Twilio webhook - always appropriate for each case
    if media_url:
        response_message = RESPONSE_MESSAGES["analyzing"]
        # Start background processing
        threading.Thread(
            target=background_task,
            args=(phone_number, incoming, media_url),
            daemon=True
        ).start()
    else:
        response_message = RESPONSE_MESSAGES["request_image"]

    # Create TwiML response
    response = MessagingResponse()
    response.message(response_message)
    return str(response)
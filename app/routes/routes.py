import threading
from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse

from app.utils.twilio_validator import validate_twilio_request
from app.services.message_processor import process_incoming
from app.services.twilio_client import send_whatsapp_message
from app.utils.logger import get_logger

bp = Blueprint("whatsapp", __name__)
logger = get_logger(__name__)

@bp.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """
    WhatsApp webhook handler with session-based conversation support.
    
    1) Validate the Twilio signature.
    2) Read incoming message & sender phone number.
    3) Spawn a background thread to handle session-based processing.
    4) Return empty TwiML immediately.
    """
    validate_twilio_request()

    incoming = request.values.get("Body", "").strip()
    sender = request.values.get("From")  # WhatsApp phone number like "whatsapp:+15551234567"
    
    # Clean phone number (remove whatsapp: prefix if present)
    phone_number = sender.replace("whatsapp:", "") if sender else ""
    
    logger.info(f"📥 Received from {phone_number}: {incoming[:100]}{'...' if len(incoming) > 100 else ''}")

    def background_task(phone: str, body: str):
        """Background task that processes the message with session context."""
        try:
            result = process_incoming(phone, body)
            
            if result.get("success"):
                reply = result.get("aiResponse", "Sorry, I couldn't process your message.")
            else:
                reply = result.get("aiResponse", "Sorry, something went wrong. Please try again.")
            
            # Send reply back to user
            send_whatsapp_message(to=sender, body=reply)  # Use original sender format for Twilio
            logger.info(f"✅ Sent reply to {phone}: {len(reply)} chars")
            
        except Exception as e:
            logger.error(f"❌ Error in background task for {phone}: {e}")
            # Send error message to user
            error_reply = "Sorry, I encountered an error processing your message. Please try again."
            try:
                send_whatsapp_message(to=sender, body=error_reply)
            except Exception as send_error:
                logger.error(f"❌ Failed to send error message: {send_error}")

    # Start background processing
    threading.Thread(
        target=background_task,
        args=(phone_number, incoming),
        daemon=True
    ).start()

    # Always return valid TwiML immediately to acknowledge receipt
    return str(MessagingResponse())

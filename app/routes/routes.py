import threading
import os
import requests
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
    validate_twilio_request()

    incoming = request.values.get("Body", "").strip()
    sender = request.values.get("From")
    media_url = request.form.get('MediaUrl0')
    phone_number = sender.replace("whatsapp:", "") if sender else ""
    logger.info(f"📥 Received Text from {phone_number}: {incoming[:100]}{'...' if len(incoming) > 100 else ''}")

    def background_task(phone: str):
        if media_url:
            logger.info(f"📥 Received Media from {phone_number}: {media_url}")

            # Twilio credentials for Basic Auth
            twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")

            try:
                # Use HTTP Basic Auth with Twilio credentials to download the image
                resp = requests.get(media_url, auth=(twilio_account_sid, twilio_auth_token))
                resp.raise_for_status()

                save_folder = "saved_images"
                os.makedirs(save_folder, exist_ok=True)

                import time
                filename = f"{phone_number}_{int(time.time())}.jpg"
                filepath = os.path.join(save_folder, filename)

                with open(filepath, 'wb') as f:
                    f.write(resp.content)

                logger.info(f"✅ Saved image to {filepath}")
            except Exception as e:
                logger.error(f"❌ Failed to download or save image: {e}")
                send_whatsapp_message(phone_number, "There was an error processing your image. Please try again.")    

    # Start background processing
    threading.Thread(
        target=background_task,
        args=(phone_number,),
        daemon=True
    ).start()

    if media_url:
        # Log and acknowledge the received media
        logger.info(f"📥 Received Media from {phone_number}: {media_url}")
        response_message = "Thank you! Your image was received."
    elif incoming:
        # Log and request media if only text was received
        logger.info(f"📥 No media received from {phone_number}, but text was: '{incoming}'")
        response_message = "Please send an image!"
    else:
        # Log if nothing meaningful was received
        logger.warning(f"⚠️ Empty message received from {phone_number}")
        response_message = "We couldn't detect any image or text. Please try again."

    # Create TwiML response
    response = MessagingResponse()
    response.message(response_message)
    return str(response)
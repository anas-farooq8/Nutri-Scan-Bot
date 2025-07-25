import time
from app.utils.logger import get_logger
from app.services.openai_client import nutrition_analyzer
from app.utils.image_handler import download_image_stream

logger = get_logger(__name__)

def process_incoming(phone_number: str, text: str, media_url: str, twilio_account_sid: str, twilio_auth_token: str) -> dict:
    """
    Process incoming WhatsApp message with media using memory-efficient streaming.
    
    Args:
        phone_number (str): Phone number of the sender
        text (str): Text message content
        media_url (str): Twilio media URL
        twilio_account_sid (str): Twilio Account SID
        twilio_auth_token (str): Twilio Auth Token
    
    Returns:
        dict: Result with success status and AI response
    """
    logger.info(f"📱 Processing media message from {phone_number}")
    
    try:
        total_start = time.time()
        
        # Measure download time
        download_start = time.time()
        # Use context manager to ensure immediate memory cleanup
        with download_image_stream(media_url, twilio_account_sid, twilio_auth_token) as base64_image:
            download_duration = time.time() - download_start
            logger.info(f"📥 Image downloaded in {download_duration:.2f}s")

            # Measure OpenAI processing time
            openai_start = time.time()
            # Process the image immediately while in context
            result = nutrition_analyzer.analyze_nutrition_label_from_base64(base64_image)
            openai_duration = time.time() - openai_start
            logger.info(f"🤖 OpenAI analysis took {openai_duration:.2f}s")

        # Measure total time
        total_duration = time.time() - total_start
        logger.info(f"⏱️ Total process took {total_duration:.2f}s (Download: {download_duration:.2f}s + OpenAI: {openai_duration:.2f}s), success={result.get('success')}")

        if result.get("tokens_used"):
            logger.info(f"🎫 Tokens used: {result['tokens_used']}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Error processing media for {phone_number}: {e}")
        return {
            "success": False,
            "aiResponse": "Sorry, I encountered an error analyzing your nutrition label. Please make sure the image is clear and try again."
        }

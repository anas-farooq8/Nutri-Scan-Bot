import base64
import requests
from contextlib import contextmanager
from app.utils.logger import get_logger

logger = get_logger(__name__)

@contextmanager
def download_image_stream(media_url: str, twilio_account_sid: str, twilio_auth_token: str):
    """
    Context manager to download image data as a stream and automatically clean up.
    This avoids keeping large base64 strings in memory.
    
    Args:
        media_url (str): Twilio media URL
        twilio_account_sid (str): Twilio Account SID for authentication
        twilio_auth_token (str): Twilio Auth Token for authentication
        
    Yields:
        str: Base64 encoded image data (automatically cleaned up after use)
        
    Raises:
        Exception: If download or encoding fails
    """
    response = None
    base64_image = None
    
    try:
        logger.info(f"📥 Downloading image from Twilio URL (streaming)")
        
        # Use HTTP Basic Auth with Twilio credentials to download the image
        response = requests.get(media_url, auth=(twilio_account_sid, twilio_auth_token))
        response.raise_for_status()
        
        # Convert to base64 immediately
        base64_image = base64.b64encode(response.content).decode('utf-8')
        
        # Clear the response content from memory immediately
        response.close()
        response = None
        
        logger.info(f"✅ Image downloaded and encoded. Size: {len(base64_image)} chars")
        
        # Yield the base64 data for immediate use
        yield base64_image
        
    except requests.RequestException as e:
        logger.error(f"❌ Failed to download image from {media_url}: {e}")
        raise Exception(f"Failed to download image: {e}")
    except Exception as e:
        logger.error(f"❌ Failed to process image: {e}")
        raise Exception(f"Failed to process image: {e}")
    finally:
        # Explicit cleanup
        if response:
            response.close()
        if base64_image:
            del base64_image  # Explicit deletion to help garbage collection
        logger.info(f"🗑️ Image data cleaned from memory")

import time
from app.utils.logger import get_logger

# Initialize session-based AYD client
logger = get_logger(__name__)

def process_incoming(phone_number: str, text: str) -> dict:
    """
    Process incoming WhatsApp message with session-based conversation support.
    Simple approach: just get the response and return it.
    """
    logger.info(f"📱 Processing message from {phone_number}: {text[:50]}{'...' if len(text) > 50 else ''}")
    
    # Call AYD with session context
    start = time.time()
    result = None # openai client
    duration = time.time() - start
    
    logger.info(f"🔍 Openai call took {duration:.2f}s, success={result.get('success')}")
    
    return result

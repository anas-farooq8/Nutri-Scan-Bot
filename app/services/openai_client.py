import base64
from openai import OpenAI
from app.settings.config import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)

class NutritionAnalyzerClient:
    """
    OpenAI client specifically designed for analyzing nutritional labels of kids' snacks.
    Uses GPT-4 Vision to process images and provide nutritional and allergy advice.
    """
    
    def __init__(self):
        """Initialize the OpenAI client with configuration."""
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        # Load nutrition analysis prompt from configuration
        self.nutrition_prompt = Config.NUTRITION_PROMPT
    
    def analyze_nutrition_label_from_base64(self, base64_image: str) -> dict:
        """
        Analyze a nutritional label from base64 encoded image data.
        Note: This method processes the image immediately and doesn't store the base64 data.
        
        Args:
            base64_image (str): Base64 encoded image data
            
        Returns:
            dict: Analysis result with success status and AI response
        """
        try:
            logger.info(f"🔍 Starting nutrition analysis from base64 data (60s timeout)")
            
            # Prepare the vision request with base64 data
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self.nutrition_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=600,
                temperature=0.5,
                timeout=60  # 60 seconds timeout for the request
            )
            
            # Extract the response
            ai_response = response.choices[0].message.content
            
            logger.info(f"✅ OpenAI analysis completed successfully. Response length: {len(ai_response)} chars")
            
            # Explicitly clear the base64 data from the request
            del base64_image
            
            return {
                "success": True,
                "aiResponse": ai_response,
                "tokens_used": response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            logger.error(f"❌ OpenAI analysis failed for base64 data: {e}")
            
            # Check if it's a timeout error
            error_message = str(e).lower()
            if "timeout" in error_message or "timed out" in error_message:
                ai_response = "Sorry, the analysis took too long and timed out. Please try again with a clearer image."
                logger.warning(f"⏰ OpenAI request timed out after 60 seconds")
            else:
                ai_response = "Sorry, I couldn't analyze the nutritional label. Please make sure the image is clear and shows the nutrition facts clearly, then try again."
            
            return {
                "success": False,
                "aiResponse": ai_response,
                "error": str(e)
            }
        finally:
            # Ensure cleanup even if there's an error
            try:
                del base64_image
            except:
                pass

# Global instance for use across the application
nutrition_analyzer = NutritionAnalyzerClient()

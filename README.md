# Nutri-Scan Bot

A WhatsApp chatbot that analyzes nutritional labels of kids' snacks using OpenAI GPT-4 Vision. Built with Flask and Twilio for seamless WhatsApp integration.

## Features

- **AI-Powered Nutrition Analysis**: Uses GPT-4 Vision to analyze nutrition labels from photos
- **WhatsApp Integration**: Seamless messaging through Twilio with 15-second webhook timeout compliance
- **Child-Focused Guidance**: Specifically tailored advice for children's snack evaluation
- **Allergy Detection**: Identifies allergens and cross-contamination risks
- **Non-Conversational Design**: Always requests an image if none is provided
- **Memory-Efficient Processing**: Streams images without local storage using base64 encoding
- **Character Limit Handling**: Respects WhatsApp's 1600 character message limit

## Architecture

The application follows a webhook-based architecture with background processing to handle Twilio's 15-second timeout requirement:

```
WhatsApp User → Twilio Webhook (15s timeout) → Flask App → Background Thread → OpenAI GPT-4 Vision → Response
```

### Twilio Webhook Constraints

- **15-Second Timeout**: Twilio requires webhook responses within 15 seconds
- **Immediate TwiML Response**: App returns empty TwiML immediately to avoid timeout
- **Background Processing**: Image analysis happens asynchronously in separate thread
- **Character Limit**: WhatsApp messages limited to 1600 characters maximum

### OpenAI Integration

- **Endpoint**: Uses OpenAI Chat Completions API with vision capabilities
- **Image Format**: Images converted to base64 encoding for API submission
- **Model**: GPT-4 Vision (gpt-4o-mini) with 60-second timeout
- **Processing**: Direct base64 image analysis without local file storage

## How It Works

### Complete Workflow

1. **Message Reception**: User sends WhatsApp message to Twilio number along with a picture
2. **Webhook Call**: Twilio sends POST request to `/whatsapp` endpoint
3. **Immediate Response**: Flask returns empty TwiML within 15-second limit
4. **Background Thread**: If image present, spawn background processing thread
5. **Image Download**: Download image from Twilio's MediaUrl using requests
6. **Base64 Conversion**: Convert downloaded image bytes to base64 string
7. **OpenAI API Call**: Send base64 image to GPT-4 Vision API with nutrition analysis prompt
8. **Response Processing**: Parse OpenAI response and format for WhatsApp
9. **Character Limit Check**: Ensure response fits within 1600 character limit
10. **WhatsApp Reply**: Send analysis back via Twilio REST API

### No Image Workflow

1. **Text Message**: User sends text without image
2. **Immediate Request**: Bot responds: "Please send me a photo of the nutrition label you'd like me to analyze! 📸"

## Project Structure

```
Nutri-Scan-Bot/
├── app/
│   ├── __init__.py              # Flask application factory
│   ├── routes/
│   │   └── routes.py            # Webhook endpoint handler
│   ├── services/
│   │   ├── message_processor.py # Core message processing logic
│   │   ├── openai_client.py     # OpenAI GPT-4 Vision client
│   │   └── twilio_client.py     # Twilio messaging service
│   ├── settings/
│   │   └── config.py            # Configuration management
│   └── utils/
│       ├── image_handler.py     # Memory-efficient image processing
│       ├── logger.py            # Application logging
│       └── twilio_validator.py  # Webhook signature validation
├── saved_images/                # Local image storage (for testing)
├── logs/                        # Application log files
├── requirements.txt             # Python dependencies
├── run.py                      # Application entry point
├── test_nutrition.py           # Local testing script
└── README.md                   # This file
```

## Configuration

Create a `.env` file with the following variables:

```env
# Twilio Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_FROM_NUMBER=+xxxxxxxxxxx

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=5000
```

## Quick Setup

1. **Create and activate virtual environment**:

   **Windows:**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **Linux/macOS:**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:

   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Run the application**:

   ```bash
   python run.py
   ```

5. **Set webhook in Twilio Console**:
   - Navigate to Messaging → Try it out → Send a WhatsApp message
   - Set webhook URL to: `https://your-domain.com/whatsapp`

## Dependencies

```
flask==2.3.3          # Web framework
twilio==8.10.3         # WhatsApp messaging
python-dotenv==1.0.0   # Environment variables
openai==1.12.0         # OpenAI client
requests==2.31.0       # HTTP client
gunicorn==21.2.0       # Production WSGI server
```

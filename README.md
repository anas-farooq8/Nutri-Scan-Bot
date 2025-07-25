# 🥨 Nutri-Scan Bot

A WhatsApp chatbot that analyzes nutritional labels of kids' snacks using AI vision technology. Simply send a photo of a nutrition label, and get instant nutritional advice and allergy information!

## 🎯 Features

- **📸 Image Analysis**: Send photos of nutrition labels via WhatsApp
- **🤖 AI-Powered**: Uses GPT-4 Vision to analyze nutritional content
- **👶 Kid-Focused**: Specifically designed for children's snack analysis
- **⚠️ Allergy Detection**: Identifies allergens and cross-contamination risks
- **📊 Parent-Friendly**: Provides clear, actionable advice for busy parents
- **⚡ Fast Response**: Immediate acknowledgment with analysis in seconds

## 🏗️ Architecture

```
📱 WhatsApp → 🌐 Twilio → 🚀 Flask App → 🤖 OpenAI GPT-4 Vision → 📊 Analysis
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- OpenAI API key
- Twilio account with WhatsApp sandbox/approved number
- ngrok or similar tunneling service for local development

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Nutri-Scan-Bot

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your credentials:

   ```env
   # Twilio Configuration
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_FROM_NUMBER=+14155238886
   TWILIO_WEBHOOK_URL=https://your-domain.ngrok.io/whatsapp

   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-4o-mini

   # Flask Configuration
   FLASK_ENV=development
   FLASK_DEBUG=True
   HOST=0.0.0.0
   PORT=5000
   ```

### 4. Testing

Test the nutrition analysis locally:

```bash
python test_nutrition.py
```

### 5. Run the Application

```bash
python run.py
```

### 6. Set up Webhook

1. Use ngrok to expose your local server:

   ```bash
   ngrok http 5000
   ```

2. Update your Twilio webhook URL to: `https://your-ngrok-url.ngrok.io/whatsapp`

## 📋 How It Works

### User Experience

1. **📱 Send Photo**: User sends a photo of a nutrition label via WhatsApp
2. **⏳ Processing**: Bot acknowledges receipt and processes the image
3. **📊 Analysis**: AI analyzes the nutritional content and allergens
4. **💬 Response**: User receives detailed nutritional advice

### Technical Flow

1. **Webhook Reception**: Twilio forwards WhatsApp message to Flask app
2. **Image Download**: App downloads image from Twilio's media URL
3. **AI Processing**: OpenAI GPT-4 Vision analyzes the nutrition label
4. **Response Generation**: Structured nutritional advice is generated
5. **Message Delivery**: Response sent back via Twilio WhatsApp API

## 🔧 API Endpoints

### `/whatsapp` (POST)

Webhook endpoint for Twilio WhatsApp messages.

**Request Body** (from Twilio):

- `Body`: Text message content
- `From`: Sender's WhatsApp number
- `MediaUrl0`: URL to attached media (if any)

**Response**: TwiML response for immediate acknowledgment

## 📁 Project Structure

```
Nutri-Scan-Bot/
├── app/
│   ├── __init__.py              # Application factory
│   ├── routes/
│   │   └── routes.py            # WhatsApp webhook routes
│   ├── services/
│   │   ├── message_processor.py # Message processing logic
│   │   ├── openai_client.py     # OpenAI vision client
│   │   └── twilio_client.py     # Twilio messaging client
│   ├── settings/
│   │   └── config.py            # Configuration management
│   └── utils/
│       ├── logger.py            # Logging utilities
│       └── twilio_validator.py  # Webhook validation
├── saved_images/                # Downloaded images storage
├── logs/                        # Application logs
├── requirements.txt             # Python dependencies
├── run.py                      # Application entry point
├── test_nutrition.py           # Testing script
└── .env.example                # Environment template
```

## 🧪 Testing

### Local Image Testing

1. Place nutrition label images in `saved_images/` folder
2. Run: `python test_nutrition.py`

### WhatsApp Testing

1. Start the Flask app: `python run.py`
2. Expose with ngrok: `ngrok http 5000`
3. Update Twilio webhook URL
4. Send photos to your Twilio WhatsApp number

## 🔐 Security Features

- **Webhook Validation**: Validates Twilio webhook signatures
- **Environment Variables**: Sensitive data stored in environment variables
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Rate Limiting**: Background processing prevents webhook timeouts

## 📊 Sample Analysis Output

```
🔍 NUTRITIONAL ANALYSIS:
- Overall nutritional quality: Fair
- High sugar content (12g per serving) - consider limiting frequency
- Low fiber content (1g)
- Contains some beneficial vitamins

⚠️ ALLERGY INFORMATION:
- Contains: Wheat, Milk, Soy
- May contain: Tree nuts, Peanuts

👶 PARENT GUIDANCE:
- Suitable for children 3+ years
- Limit to 1-2 times per week as an occasional treat
- Better as an after-school snack than breakfast

📊 QUICK VERDICT:
Decent occasional snack but high in sugar - pair with fruit for better nutrition.
```

## 🚀 Deployment

### Environment Variables for Production

```env
FLASK_ENV=production
FLASK_DEBUG=False
HOST=0.0.0.0
PORT=8080
```

### Deployment Options

- **Heroku**: Use `Procfile` with gunicorn
- **Azure App Service**: Deploy with container or code
- **AWS Elastic Beanstalk**: Python application deployment
- **Google Cloud Run**: Containerized deployment

## 🔧 Configuration Options

### OpenAI Settings

- `OPENAI_MODEL`: Model to use (default: `gpt-4o-mini`)
- Higher detail level for better text recognition in nutrition labels

### Twilio Settings

- `MAX_SMS_CHARS`: Maximum message length (default: 1600)
- Automatic message splitting for longer responses

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Errors**

   - Check API key validity
   - Verify account has sufficient credits
   - Ensure model availability

2. **Twilio Webhook Issues**

   - Verify webhook URL is accessible
   - Check Twilio signature validation
   - Ensure HTTPS for production

3. **Image Processing Issues**
   - Check image format compatibility
   - Verify image URL accessibility
   - Ensure sufficient image quality

### Debug Mode

Set `FLASK_DEBUG=True` in `.env` for detailed error messages.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For issues and questions:

- Create an issue in this repository
- Check the troubleshooting section above
- Review Twilio and OpenAI documentation

---

**Made with ❤️ for better nutrition decisions**

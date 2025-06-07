# Instructions to Recreate DataDrape AI - Multimodal Chat Interface

## Project Overview

Create a multimodal AI chat interface that:
- Uses OpenRouter API with Google's Gemini 2.5 Flash Preview model (`google/gemini-2.5-flash-preview-05-20`)
- Supports text and image inputs (upload, paste, URL)
- Has a Flask backend that securely handles API keys
- Features a modern dark-themed UI with streaming responses
- Includes Docker support and production deployment configurations

## Project Structure

Create the following directory structure:

```
datadrape-ai/
├── index.html           # Frontend UI
├── app.py              # Backend server
├── requirements.txt    # Python dependencies
├── .env.example       # Environment template
├── .gitignore         # Git ignore rules
├── README.md          # Documentation
├── run.sh            # Linux/Mac startup
├── run.bat           # Windows startup
├── test_openrouter.py # API test script
├── Dockerfile        # Docker config
├── docker-compose.yml # Docker Compose
├── gunicorn_config.py # Production server
├── nginx.conf.example # Nginx config
├── datadrape.service # Systemd service
├── deployment.md     # Deployment guide
├── CNAME            # GitHub Pages domain
└── temp_uploads/     # Image uploads (auto-created)
```

## Step-by-Step Implementation

### 1. Create the Frontend (index.html)

Create a single-page application with:

**Key Features:**
- Dark theme with animated gradient background
- Collapsible system prompt (hidden by default)
- Image support (upload button, paste from clipboard, URL input)
- Streaming message display
- Export chat functionality
- Auto-resizing text input

**Technical Requirements:**
- Use CSS variables for theming
- Implement Server-Sent Events (SSE) for streaming
- Handle multimodal message format:
  ```javascript
  {
    role: "user",
    content: [
      { type: "text", text: "message" },
      { type: "image_url", image_url: { url: "..." } }
    ]
  }
  ```
- Auto-detect backend URL (file:// vs served)
- Include image preview with remove option
- Add modal for image URL input
- Implement status notifications

**UI Components:**
- Header with title "DataDrape AI" and model badge
- Collapsible system prompt section
- Chat area with messages container
- Input area with image controls and message input
- Control buttons (Clear Chat, Export Chat)
- Floating status indicator

### 2. Create the Backend (app.py)

Build a Flask server with:

**Core Functionality:**
- Environment variable loading (python-dotenv)
- CORS support for development
- Async request handling with aiohttp
- Server-Sent Events streaming
- Image upload endpoint
- Health check endpoint

**API Endpoints:**
- `GET /` - Serve frontend
- `POST /api/chat` - Handle chat with streaming
- `POST /api/upload-image` - Handle image uploads
- `GET /health` - Health check

**OpenRouter Integration:**
- Model: `google/gemini-2.5-flash-preview-05-20`
- Headers:
  ```python
  {
    'Authorization': f'Bearer {OPENROUTER_API_KEY}',
    'HTTP-Referer': 'https://datadrape.com',
    'X-Title': 'DataDrape AI'
  }
  ```
- Support multimodal messages with proper content array format
- Stream responses using SSE format

### 3. Create Supporting Files

**requirements.txt:**
```
flask==3.0.0
flask-cors==4.0.0
aiohttp==3.9.1
python-dotenv==1.0.0
gunicorn==21.2.0
```

**.env.example:**
```
OPENROUTER_API_KEY=your-openrouter-api-key-here
SITE_URL=https://datadrape.com
SITE_NAME=DataDrape AI
```

**.gitignore:**
Include standard Python ignores plus:
- .env files
- temp_uploads/
- venv/
- __pycache__/
- IDE files

### 4. Create Startup Scripts

**run.sh (Linux/Mac):**
- Check for .env file
- Create/activate virtual environment
- Install dependencies
- Run API test
- Start server if test passes

**run.bat (Windows):**
- Same functionality as run.sh but for Windows

**test_openrouter.py:**
- Test basic text request
- Test image analysis
- Verify API key and model access

### 5. Create Docker Configuration

**Dockerfile:**
- Base: python:3.11-slim
- Install system dependencies
- Copy and install requirements
- Set up health check
- Run with gunicorn

**docker-compose.yml:**
- Service configuration
- Environment variables
- Volume for temp_uploads
- Health check settings
- Optional nginx service

**gunicorn_config.py:**
- Worker configuration
- Logging settings
- Environment variables

### 6. Create Production Files

**nginx.conf.example:**
- SSL configuration
- Proxy settings for SSE
- Security headers
- Static file caching

**datadrape.service:**
- Systemd service configuration
- Security settings
- Restart policies

### 7. Create Documentation

**README.md:**
- Project overview
- Features list
- Installation instructions
- Usage guide
- Deployment options

**deployment.md:**
- Local development setup
- Docker deployment
- VPS deployment with nginx
- GitHub Pages + backend service
- SSL setup instructions

## Key Implementation Details

### Message Format
The system must support OpenRouter's exact multimodal format:

```json
{
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is in this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://example.com/image.jpg"
          }
        }
      ]
    }
  ]
}
```

### Streaming Response Format
Use Server-Sent Events with format:
```
data: {"content": "response text"}
data: [DONE]
```

### Security Considerations
- Never expose API key in frontend
- Use environment variables
- Enable CORS only for development
- Validate file uploads (type, size)
- Use secure headers in production

### UI/UX Requirements
- Dark theme (#0a0a0a background)
- Indigo accent color (#6366f1)
- Smooth animations (300ms transitions)
- Responsive design
- Custom scrollbars
- Loading indicators

## Testing Checklist

1. ✓ API connection works
2. ✓ Text messages send/receive
3. ✓ Images upload successfully
4. ✓ Image URLs work
5. ✓ Clipboard paste works
6. ✓ Streaming displays properly
7. ✓ System prompt is configurable
8. ✓ Chat can be cleared
9. ✓ Chat can be exported
10. ✓ Error handling works

## Deployment Verification

1. Environment variables load correctly
2. Backend serves frontend at root
3. API endpoints are accessible
4. CORS is properly configured
5. SSL works (if applicable)
6. Streaming works through proxy
7. File uploads work
8. Health check passes

## Important Notes

- The model MUST be exactly: `google/gemini-2.5-flash-preview-05-20`
- System prompt is hidden by default (user must click to expand)
- Backend handles all OpenRouter communication
- Support multiple images per message
- Images can be data URLs or external URLs
- Maximum file size is 10MB
- Temporary files are cleaned up after processing

## Success Criteria

The implementation is successful when:
1. Users can chat with text only
2. Users can upload/paste/link images
3. The AI can analyze images and respond
4. Responses stream in real-time
5. The UI is smooth and responsive
6. API keys are never exposed
7. The app can be deployed with Docker
8. Production deployment works with nginx/SSL

Remember: This is a production-ready application, not a prototype. Include proper error handling, logging, and security measures throughout.
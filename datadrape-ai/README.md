# DataDrape AI - Multimodal Chat Interface

A modern, production-ready multimodal AI chat interface powered by Google's Gemini 2.5 Flash Preview model through OpenRouter API.

## Features

- **Multimodal Support**: Chat with text and images (upload, paste, or URL)
- **Streaming Responses**: Real-time response streaming with Server-Sent Events (SSE)
- **Dark Theme UI**: Modern, animated gradient interface
- **Image Support**: 
  - Direct file upload
  - Paste from clipboard
  - URL input
  - Multiple images per message
- **Production Ready**: Docker support, nginx configuration, systemd service
- **Export Functionality**: Download chat history as JSON
- **Secure**: API keys handled server-side only

## Quick Start

### Prerequisites

- Python 3.8+ or Docker
- OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai))

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/datadrape-ai.git
cd datadrape-ai
```

2. Copy environment template:
```bash
cp .env.example .env
```

3. Edit `.env` and add your OpenRouter API key:
```bash
OPENROUTER_API_KEY=your-actual-api-key-here
```

4. Run the startup script:

**Linux/Mac:**
```bash
./run.sh
```

**Windows:**
```bash
run.bat
```

5. Open your browser to `http://localhost:5000`

### Docker Deployment

1. Ensure `.env` file is configured with your API key

2. Build and run with Docker Compose:
```bash
docker-compose up -d
```

3. Access at `http://localhost:5000`

## Usage

### Basic Chat
1. Type your message in the input field
2. Press Enter or click Send
3. Watch the AI response stream in real-time

### Using Images
- **Upload**: Click the camera button and select an image
- **Paste**: Use Ctrl+V to paste images from clipboard
- **URL**: Click the link button and enter an image URL

### System Prompt
- Click "System Prompt" to expand the configuration
- Customize the AI's behavior and responses
- Changes apply to new conversations

### Export Chat
- Click "Export Chat" to download conversation history
- Saved as JSON with timestamps

## Project Structure

```
datadrape-ai/
├── index.html           # Frontend UI
├── app.py              # Backend server
├── requirements.txt    # Python dependencies
├── .env.example       # Environment template
├── .gitignore         # Git ignore rules
├── README.md          # This file
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
└── temp_uploads/     # Image uploads
```

## Configuration

### Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)
- `SITE_URL`: Your site URL (default: https://datadrape.com)
- `SITE_NAME`: Your site name (default: DataDrape AI)
- `PORT`: Server port (default: 5000)
- `FLASK_ENV`: Set to `development` for debug mode

### Model

The application uses Google's Gemini 2.5 Flash Preview model:
- Model ID: `google/gemini-2.5-flash-preview-05-20`
- Supports text and image inputs
- Fast response times
- Cost-effective for production use

## Development

### Running Tests

Test the OpenRouter API connection:
```bash
python test_openrouter.py
```

### Making Changes

1. Frontend changes: Edit `index.html`
2. Backend changes: Edit `app.py`
3. Restart the server to see changes

### Adding Features

The codebase is designed to be extensible:
- Add new API endpoints in `app.py`
- Extend the UI in `index.html`
- Modify styles using CSS variables

## Deployment Options

See [deployment.md](deployment.md) for detailed instructions on:
- Docker deployment
- VPS deployment with nginx
- GitHub Pages + backend service
- SSL/TLS configuration

## Security

- API keys are never exposed to the frontend
- File uploads are validated and size-limited (10MB)
- Temporary files are cleaned up after processing
- CORS enabled only in development mode
- Production uses secure headers and HTTPS

## Troubleshooting

### API Connection Issues
- Verify your OpenRouter API key is correct
- Check internet connectivity
- Run `python test_openrouter.py` to diagnose

### Image Upload Problems
- Ensure images are under 10MB
- Supported formats: PNG, JPG, JPEG, GIF, WebP, BMP
- Check `temp_uploads/` directory has write permissions

### Streaming Not Working
- Ensure your proxy/firewall allows SSE connections
- Check nginx configuration if using reverse proxy
- Disable buffering for `/api/chat` endpoint

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and feature requests, please use the GitHub issue tracker.

---

Built with ❤️ using Flask, OpenRouter API, and modern web technologies.
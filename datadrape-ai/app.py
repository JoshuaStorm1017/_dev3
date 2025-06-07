import os
import json
import asyncio
import aiohttp
from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import base64
import tempfile
from werkzeug.utils import secure_filename
import time
from datetime import datetime, timezone

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Enable CORS
ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', '*').split(',')
CORS(app, origins=ALLOWED_ORIGINS)

# Configuration
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
SITE_URL = os.environ.get('SITE_URL', 'https://datadrape.com')
SITE_NAME = os.environ.get('SITE_NAME', 'DataDrape AI')
MODEL = 'google/gemini-2.5-flash-preview-05-20'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Ensure temp directory exists
UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'model': MODEL
    })

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    """Handle image uploads"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': 'File too large. Maximum size is 10MB'}), 400
    
    try:
        # Save temporarily and convert to base64
        filename = secure_filename(f"{int(time.time())}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Read and encode
        with open(filepath, 'rb') as f:
            image_data = f.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
            mime_type = f"image/{filename.rsplit('.', 1)[1].lower()}"
            data_url = f"data:{mime_type};base64,{base64_image}"
        
        # Clean up
        os.remove(filepath)
        
        return jsonify({'url': data_url})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests with streaming response"""
    if not OPENROUTER_API_KEY:
        return jsonify({'error': 'OpenRouter API key not configured'}), 500
    
    try:
        data = request.json
        messages = data.get('messages', [])
        
        if not messages:
            return jsonify({'error': 'No messages provided'}), 400
        
        # Process messages to ensure proper format
        processed_messages = []
        for msg in messages:
            if isinstance(msg.get('content'), list):
                # Already in correct format
                processed_messages.append(msg)
            else:
                # Convert string content to array format
                processed_messages.append({
                    'role': msg['role'],
                    'content': [{'type': 'text', 'text': msg['content']}]
                })
        
        def generate():
            """Generate SSE stream"""
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def stream_response():
                headers = {
                    'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                    'HTTP-Referer': SITE_URL,
                    'X-Title': SITE_NAME,
                    'Content-Type': 'application/json'
                }
                
                payload = {
                    'model': MODEL,
                    'messages': processed_messages,
                    'stream': True
                }
                
                async with aiohttp.ClientSession() as session:
                    try:
                        async with session.post(
                            'https://openrouter.ai/api/v1/chat/completions',
                            headers=headers,
                            json=payload
                        ) as response:
                            if response.status != 200:
                                error_text = await response.text()
                                yield f"data: {json.dumps({'error': f'API error: {error_text}'})}\n\n"
                                return
                            
                            async for line in response.content:
                                line = line.decode('utf-8').strip()
                                if line.startswith('data: '):
                                    data = line[6:]
                                    if data == '[DONE]':
                                        yield "data: [DONE]\n\n"
                                        break
                                    
                                    try:
                                        parsed = json.loads(data)
                                        if 'choices' in parsed and len(parsed['choices']) > 0:
                                            delta = parsed['choices'][0].get('delta', {})
                                            if 'content' in delta:
                                                yield f"data: {json.dumps({'content': delta['content']})}\n\n"
                                    except json.JSONDecodeError:
                                        continue
                    
                    except Exception as e:
                        yield f"data: {json.dumps({'error': str(e)})}\n\n"
            
            # Run the async function
            try:
                # Create coroutine and run it
                async_gen = stream_response()
                while True:
                    try:
                        chunk = loop.run_until_complete(async_gen.__anext__())
                        yield chunk
                    except StopAsyncIteration:
                        break
            finally:
                loop.close()
        
        return Response(
            generate(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'  # Disable nginx buffering
            }
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
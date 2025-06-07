#!/usr/bin/env python3
"""
Test script for OpenRouter API connection
Tests both text and image capabilities
"""

import os
import sys
import json
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
MODEL = 'google/gemini-2.5-flash-preview-05-20'

async def test_text_request():
    """Test basic text request"""
    print("Testing text request...")
    
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'HTTP-Referer': 'https://datadrape.com',
        'X-Title': 'DataDrape AI Test',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': MODEL,
        'messages': [
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': 'Say "Hello, DataDrape AI is working!" and nothing else.'
                    }
                ]
            }
        ],
        'stream': False
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data['choices'][0]['message']['content']
                    print(f"✓ Text test passed: {content}")
                    return True
                else:
                    error = await response.text()
                    print(f"✗ Text test failed: {error}")
                    return False
        except Exception as e:
            print(f"✗ Text test error: {str(e)}")
            return False

async def test_image_request():
    """Test image analysis capability"""
    print("\nTesting image analysis...")
    
    # Use a simple base64 encoded 1x1 red pixel as test image
    test_image_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'HTTP-Referer': 'https://datadrape.com',
        'X-Title': 'DataDrape AI Test',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': MODEL,
        'messages': [
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': 'This is a test image. Please respond with: "Image test successful"'
                    },
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': test_image_base64
                        }
                    }
                ]
            }
        ],
        'stream': False
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data['choices'][0]['message']['content']
                    print(f"✓ Image test passed: {content}")
                    return True
                else:
                    error = await response.text()
                    print(f"✗ Image test failed: {error}")
                    print("Note: Some models may have image support disabled or limited.")
                    print("The application will still work for text chat.")
                    return False
        except Exception as e:
            print(f"✗ Image test error: {str(e)}")
            return False

async def main():
    """Run all tests"""
    print("DataDrape AI - OpenRouter API Test")
    print("==================================")
    print(f"Model: {MODEL}")
    
    if not OPENROUTER_API_KEY:
        print("\n✗ Error: OPENROUTER_API_KEY not found in environment")
        print("Please ensure .env file contains your API key")
        return False
    
    print(f"API Key: {OPENROUTER_API_KEY[:8]}...{OPENROUTER_API_KEY[-4:]}")
    print()
    
    # Run tests
    text_result = await test_text_request()
    image_result = await test_image_request()
    
    # Summary
    print("\nTest Summary:")
    print("=============")
    print(f"Text capability: {'✓ Passed' if text_result else '✗ Failed'}")
    print(f"Image capability: {'✓ Passed' if image_result else '✗ Failed'}")
    
    return text_result and image_result

if __name__ == '__main__':
    # Run the async main function
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
#!/bin/bash

echo "DataDrape AI - Setup and Launch Script"
echo "======================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and add your OpenRouter API key:"
    echo "  cp .env.example .env"
    echo "  nano .env  # or use your preferred editor"
    exit 1
fi

# Check if API key is set
if grep -q "your-openrouter-api-key-here" .env; then
    echo "Error: OpenRouter API key not configured!"
    echo "Please edit .env and add your actual API key"
    exit 1
fi

# Detect Python command (python3 or python)
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "Error: Python not found. Please install Python 3.8+"
    exit 1
fi

echo "Using Python: $PYTHON_CMD"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Test API connection
echo ""
echo "Testing OpenRouter API connection..."
python test_openrouter.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Warning: Some tests failed, but continuing anyway..."
    echo "The app will still work for text chat!"
    echo ""
fi

# Start the server
echo ""
echo "Starting DataDrape AI server..."
echo "Access the interface at: http://localhost:5000"
echo ""
echo "In WSL, you can also access it from Windows at:"
echo "  http://localhost:5000"
echo "  http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

export FLASK_ENV=development
python app.py
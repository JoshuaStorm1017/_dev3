@echo off
echo DataDrape AI - Setup and Launch Script
echo ======================================

REM Check if .env file exists
if not exist .env (
    echo Error: .env file not found!
    echo Please copy .env.example to .env and add your OpenRouter API key:
    echo   copy .env.example .env
    echo   notepad .env
    exit /b 1
)

REM Check if API key is set
findstr /C:"your-openrouter-api-key-here" .env >nul
if %errorlevel% equ 0 (
    echo Error: OpenRouter API key not configured!
    echo Please edit .env and add your actual API key
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Test API connection
echo.
echo Testing OpenRouter API connection...
python test_openrouter.py

if errorlevel 1 (
    echo.
    echo Warning: Some tests failed, but continuing anyway...
    echo The app will still work for text chat!
    echo.
)

REM Start the server
echo.
echo Starting DataDrape AI server...
echo Access the interface at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

set FLASK_ENV=development
python app.py
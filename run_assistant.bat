@echo off
echo 🤖 Voice Assistant Quick Start
echo ==============================

echo.
echo 📋 Pre-flight checklist:
echo 1. Ollama installed and running?
echo 2. Model pulled (e.g., llama3.2:7b)?
echo 3. Microphone connected?
echo 4. Python dependencies installed?

echo.
pause

echo.
echo 🚀 Starting Voice Assistant...
echo.

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️ No virtual environment found, using system Python
)

REM Check if Ollama is running
echo Checking Ollama service...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ❌ Ollama service not running!
    echo 💡 Please start Ollama with: ollama serve
    pause
    exit /b 1
) else (
    echo ✅ Ollama service is running
)

REM Run the voice assistant
python voice_assistant.py

echo.
echo 👋 Voice Assistant session ended
pause

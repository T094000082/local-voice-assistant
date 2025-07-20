@echo off
echo 🤖 Voice Assistant Quick Start
echo ==============================

REM Change to the script directory
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call .venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else if exist "venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo ⚠️ No virtual environment found, using system Python
)

echo.
echo 🚀 Starting Voice Assistant...
echo.

REM Run the voice assistant
python voice_assistant.py

echo.
echo 👋 Voice Assistant session ended
pause

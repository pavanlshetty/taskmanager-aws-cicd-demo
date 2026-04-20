@echo off
echo Setting up Task Manager App locally...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.9+ first.
    pause
    exit /b 1
)

REM Navigate to app directory
cd app

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run the app
echo Starting Task Manager App on http://localhost:5000
python app.py
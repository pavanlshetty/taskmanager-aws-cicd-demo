# Run Task Manager App Locally
Write-Host "Setting up Task Manager App locally..." -ForegroundColor Green

# Check if Python is installed
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install Python 3.9+ first." -ForegroundColor Red
    exit 1
}

# Navigate to app directory
Set-Location -Path "app"

# Create virtual environment if it doesn't exist
if (!(Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run the app
Write-Host "Starting Task Manager App on http://localhost:5000" -ForegroundColor Green
python app.py
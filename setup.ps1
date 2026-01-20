# Setup Script - Prepare your local environment
Write-Host "🔧 Azure Cost Intelligence Agent - Setup Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python is installed: $pythonVersion" -ForegroundColor Green
    
    # Check if Python version is 3.11 or higher
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
            Write-Host "⚠ Warning: Python 3.11+ is recommended. You have $pythonVersion" -ForegroundColor Yellow
        }
    }
}
catch {
    Write-Host "✗ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check Azure CLI
Write-Host ""
Write-Host "Checking Azure CLI installation..." -ForegroundColor Yellow
try {
    $azVersion = az --version 2>&1 | Select-Object -First 1
    Write-Host "✓ Azure CLI is installed" -ForegroundColor Green
}
catch {
    Write-Host "✗ Azure CLI is not installed" -ForegroundColor Red
    Write-Host "Please install from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Yellow
    exit 1
}

# Check if .env file exists
Write-Host ""
Write-Host "Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}
else {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.template" ".env"
    Write-Host "✓ .env file created" -ForegroundColor Green
    Write-Host "⚠ Please edit .env file with your Azure OpenAI credentials!" -ForegroundColor Yellow
}

# Check if virtual environment exists
Write-Host ""
Write-Host "Setting up Python virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}
else {
    Write-Host "Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment and install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray

if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
}
else {
    Write-Host "✗ Could not activate virtual environment" -ForegroundColor Red
    exit 1
}

# Summary
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Configure your environment:" -ForegroundColor White
Write-Host "   Edit .env file with your Azure credentials:" -ForegroundColor Gray
Write-Host "   - AZURE_OPENAI_ENDPOINT" -ForegroundColor Gray
Write-Host "   - AZURE_OPENAI_API_KEY" -ForegroundColor Gray
Write-Host "   - AZURE_OPENAI_DEPLOYMENT_NAME" -ForegroundColor Gray
Write-Host "   - AZURE_SUBSCRIPTION_ID" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Test locally:" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   python main.py" -ForegroundColor Gray
Write-Host "   Open: http://localhost:8000" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Deploy to Azure:" -ForegroundColor White
Write-Host "   Edit deploy.ps1 with your configuration" -ForegroundColor Gray
Write-Host "   .\deploy.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "For more details, see README.md and DEPLOYMENT.md" -ForegroundColor Cyan
Write-Host ""

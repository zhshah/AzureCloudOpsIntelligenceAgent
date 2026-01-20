# Complete Automated Deployment Script
# This script will:
# 1. Create Azure OpenAI resource with GPT-4 deployment (if needed)
# 2. Build and deploy the Cost Intelligence Agent to Azure Container Apps

param(
    [Parameter(Mandatory=$false)]
    [switch]$SkipOpenAICreation = $false,
    
    [Parameter(Mandatory=$false)]
    [string]$ExistingOpenAIEndpoint = "",
    
    [Parameter(Mandatory=$false)]
    [string]$ExistingOpenAIKey = ""
)

# Configuration
$RESOURCE_GROUP = "Az-AICost-Agent-RG"
$LOCATION = "westeurope"
$ACR_NAME = "acrcostintel$(Get-Random -Minimum 1000 -Maximum 9999)"
$CONTAINER_APP_NAME = "cost-intelligence-agent"
$ENVIRONMENT_NAME = "cost-intelligence-env"
$OPENAI_NAME = "openai-cost-intelligence-$(Get-Random -Minimum 100 -Maximum 999)"
$OPENAI_DEPLOYMENT_NAME = "gpt-4"

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   Azure Cost Intelligence Agent - Complete Deployment        ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Get subscription info
Write-Host "📋 Checking Azure subscription..." -ForegroundColor Yellow
$subscription = az account show | ConvertFrom-Json
if (-not $subscription) {
    Write-Host "❌ Not logged into Azure. Please run: az login" -ForegroundColor Red
    exit 1
}

$SUBSCRIPTION_ID = $subscription.id
Write-Host "✓ Subscription: $($subscription.name)" -ForegroundColor Green
Write-Host "✓ Subscription ID: $SUBSCRIPTION_ID" -ForegroundColor Green
Write-Host ""

Write-Host "📦 Deployment Configuration:" -ForegroundColor Cyan
Write-Host "  Resource Group: $RESOURCE_GROUP" -ForegroundColor White
Write-Host "  Location: $LOCATION" -ForegroundColor White
Write-Host "  Container Registry: $ACR_NAME" -ForegroundColor White
Write-Host "  Container App: $CONTAINER_APP_NAME" -ForegroundColor White
if (-not $SkipOpenAICreation -and -not $ExistingOpenAIEndpoint) {
    Write-Host "  Azure OpenAI: $OPENAI_NAME" -ForegroundColor White
}
Write-Host ""
Write-Host "⏳ Starting deployment in 3 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
Write-Host ""
Write-Host "🚀 Starting deployment..." -ForegroundColor Cyan
Write-Host ""

# Step 1: Create Resource Group
Write-Host "[1/9] Creating resource group..." -ForegroundColor Yellow
az group create --name $RESOURCE_GROUP --location $LOCATION --output none
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Resource group created" -ForegroundColor Green
} else {
    Write-Host "✓ Resource group already exists" -ForegroundColor Green
}

# Step 2: Create Azure OpenAI (if needed)
if ($SkipOpenAICreation -or $ExistingOpenAIEndpoint) {
    if ($ExistingOpenAIEndpoint) {
        Write-Host "[2/9] Using existing Azure OpenAI resource..." -ForegroundColor Yellow
        $AZURE_OPENAI_ENDPOINT = $ExistingOpenAIEndpoint
        $AZURE_OPENAI_API_KEY = $ExistingOpenAIKey
        Write-Host "✓ Using provided Azure OpenAI endpoint" -ForegroundColor Green
    } else {
        Write-Host "[2/9] Skipping Azure OpenAI creation (you need to provide credentials manually)..." -ForegroundColor Yellow
        $AZURE_OPENAI_ENDPOINT = Read-Host "Enter your Azure OpenAI endpoint"
        $AZURE_OPENAI_API_KEY = Read-Host "Enter your Azure OpenAI API key" -AsSecureString
        $AZURE_OPENAI_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($AZURE_OPENAI_API_KEY))
    }
} else {
    Write-Host "[2/9] Creating Azure OpenAI resource..." -ForegroundColor Yellow
    Write-Host "       This may take 2-3 minutes..." -ForegroundColor Gray
    
    az cognitiveservices account create `
        --name $OPENAI_NAME `
        --resource-group $RESOURCE_GROUP `
        --location $LOCATION `
        --kind OpenAI `
        --sku S0 `
        --yes `
        --output none 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Azure OpenAI resource created" -ForegroundColor Green
        
        # Get endpoint and key
        $AZURE_OPENAI_ENDPOINT = az cognitiveservices account show `
            --name $OPENAI_NAME `
            --resource-group $RESOURCE_GROUP `
            --query "properties.endpoint" -o tsv
        
        $AZURE_OPENAI_API_KEY = az cognitiveservices account keys list `
            --name $OPENAI_NAME `
            --resource-group $RESOURCE_GROUP `
            --query "key1" -o tsv
        
        # Deploy GPT-4 model (if available)
        Write-Host "       Deploying GPT-4 model..." -ForegroundColor Gray
        az cognitiveservices account deployment create `
            --name $OPENAI_NAME `
            --resource-group $RESOURCE_GROUP `
            --deployment-name $OPENAI_DEPLOYMENT_NAME `
            --model-name "gpt-4" `
            --model-version "0613" `
            --model-format OpenAI `
            --sku-capacity 1 `
            --sku-name "Standard" `
            --output none 2>$null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ GPT-4 model deployed" -ForegroundColor Green
        } else {
            Write-Host "⚠ GPT-4 not available, trying gpt-35-turbo..." -ForegroundColor Yellow
            $OPENAI_DEPLOYMENT_NAME = "gpt-35-turbo"
            az cognitiveservices account deployment create `
                --name $OPENAI_NAME `
                --resource-group $RESOURCE_GROUP `
                --deployment-name $OPENAI_DEPLOYMENT_NAME `
                --model-name "gpt-35-turbo" `
                --model-version "0613" `
                --model-format OpenAI `
                --sku-capacity 1 `
                --sku-name "Standard" `
                --output none
            Write-Host "✓ GPT-3.5-Turbo model deployed" -ForegroundColor Green
        }
    } else {
        Write-Host "❌ Failed to create Azure OpenAI resource" -ForegroundColor Red
        Write-Host "   This might be due to capacity or approval requirements." -ForegroundColor Yellow
        Write-Host "   You can:" -ForegroundColor Yellow
        Write-Host "   1. Request access: https://aka.ms/oai/access" -ForegroundColor Gray
        Write-Host "   2. Try a different region" -ForegroundColor Gray
        Write-Host "   3. Use existing Azure OpenAI resource" -ForegroundColor Gray
        $useExisting = Read-Host "Do you have an existing Azure OpenAI resource? (y/n)"
        if ($useExisting -eq 'y') {
            $AZURE_OPENAI_ENDPOINT = Read-Host "Enter your Azure OpenAI endpoint"
            $AZURE_OPENAI_API_KEY = Read-Host "Enter your Azure OpenAI API key" -AsSecureString
            $AZURE_OPENAI_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($AZURE_OPENAI_API_KEY))
        } else {
            Write-Host "❌ Cannot proceed without Azure OpenAI. Exiting..." -ForegroundColor Red
            exit 1
        }
    }
}

# Step 3: Create Azure Container Registry
Write-Host ""
Write-Host "[3/9] Creating Azure Container Registry..." -ForegroundColor Yellow
az acr create `
    --resource-group $RESOURCE_GROUP `
    --name $ACR_NAME `
    --sku Basic `
    --admin-enabled true `
    --output none
Write-Host "✓ ACR created" -ForegroundColor Green

# Step 4: Build and push Docker image
Write-Host ""
Write-Host "[4/9] Building and pushing Docker image..." -ForegroundColor Yellow
Write-Host "       This may take 3-5 minutes..." -ForegroundColor Gray
az acr build `
    --registry $ACR_NAME `
    --image cost-intelligence-agent:latest `
    --file Dockerfile . `
    --output none
Write-Host "✓ Image built and pushed" -ForegroundColor Green

# Step 5: Get ACR credentials
Write-Host ""
Write-Host "[5/9] Retrieving ACR credentials..." -ForegroundColor Yellow
$ACR_USERNAME = az acr credential show --name $ACR_NAME --query username -o tsv
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv
Write-Host "✓ Credentials retrieved" -ForegroundColor Green

# Step 6: Create Container Apps environment
Write-Host ""
Write-Host "[6/9] Creating Container Apps environment..." -ForegroundColor Yellow
az containerapp env create `
    --name $ENVIRONMENT_NAME `
    --resource-group $RESOURCE_GROUP `
    --location $LOCATION `
    --output none
Write-Host "✓ Environment created" -ForegroundColor Green

# Step 7: Create Container App
Write-Host ""
Write-Host "[7/9] Creating Container App..." -ForegroundColor Yellow
az containerapp create `
    --name $CONTAINER_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --environment $ENVIRONMENT_NAME `
    --image "$ACR_NAME.azurecr.io/cost-intelligence-agent:latest" `
    --registry-server "$ACR_NAME.azurecr.io" `
    --registry-username $ACR_USERNAME `
    --registry-password $ACR_PASSWORD `
    --target-port 8000 `
    --ingress external `
    --cpu 1.0 `
    --memory 2Gi `
    --min-replicas 1 `
    --max-replicas 3 `
    --env-vars `
        "AZURE_OPENAI_ENDPOINT=$AZURE_OPENAI_ENDPOINT" `
        "AZURE_OPENAI_API_KEY=$AZURE_OPENAI_API_KEY" `
        "AZURE_OPENAI_DEPLOYMENT_NAME=$OPENAI_DEPLOYMENT_NAME" `
        "AZURE_OPENAI_API_VERSION=2024-02-15-preview" `
        "AZURE_SUBSCRIPTION_ID=$SUBSCRIPTION_ID" `
        "USE_MANAGED_IDENTITY=true" `
    --system-assigned `
    --output none
Write-Host "✓ Container App created" -ForegroundColor Green

# Step 8: Configure RBAC
Write-Host ""
Write-Host "[8/9] Configuring RBAC permissions..." -ForegroundColor Yellow

$IDENTITY_ID = az containerapp show `
    --name $CONTAINER_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --query identity.principalId -o tsv

Write-Host "       Assigning Cost Management Reader role..." -ForegroundColor Gray
az role assignment create `
    --assignee $IDENTITY_ID `
    --role "Cost Management Reader" `
    --scope "/subscriptions/$SUBSCRIPTION_ID" `
    --output none

Write-Host "       Assigning Reader role..." -ForegroundColor Gray
az role assignment create `
    --assignee $IDENTITY_ID `
    --role "Reader" `
    --scope "/subscriptions/$SUBSCRIPTION_ID" `
    --output none

Write-Host "✓ RBAC configured" -ForegroundColor Green

# Step 9: Get application URL
Write-Host ""
Write-Host "[9/9] Retrieving application URL..." -ForegroundColor Yellow
$APP_URL = az containerapp show `
    --name $CONTAINER_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --query properties.configuration.ingress.fqdn -o tsv

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║               🎉 Deployment Complete!                        ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Application URL: " -ForegroundColor Cyan -NoNewline
Write-Host "https://$APP_URL" -ForegroundColor White
Write-Host ""
Write-Host "📋 Deployment Summary:" -ForegroundColor Cyan
Write-Host "  Resource Group: $RESOURCE_GROUP" -ForegroundColor White
Write-Host "  Location: $LOCATION" -ForegroundColor White
Write-Host "  Azure OpenAI: $OPENAI_DEPLOYMENT_NAME model" -ForegroundColor White
Write-Host "  Subscription: $($subscription.name)" -ForegroundColor White
Write-Host ""
Write-Host "✨ Try these questions:" -ForegroundColor Yellow
Write-Host "  • What are my Azure costs this month?" -ForegroundColor Gray
Write-Host "  • Which service costs the most?" -ForegroundColor Gray
Write-Host "  • Show me daily spending trends" -ForegroundColor Gray
Write-Host "  • List all my virtual networks" -ForegroundColor Gray
Write-Host "  • Which VMs don't have backups?" -ForegroundColor Gray
Write-Host ""
Write-Host "📊 View logs:" -ForegroundColor Yellow
Write-Host "  az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --follow" -ForegroundColor Gray
Write-Host ""
Write-Host "🔄 Update application:" -ForegroundColor Yellow
Write-Host "  1. Make code changes" -ForegroundColor Gray
Write-Host "  2. az acr build --registry $ACR_NAME --image cost-intelligence-agent:latest ." -ForegroundColor Gray
Write-Host "  3. az containerapp update --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --image $ACR_NAME.azurecr.io/cost-intelligence-agent:latest" -ForegroundColor Gray
Write-Host ""
Write-Host "🗑️  Clean up (delete everything):" -ForegroundColor Yellow
Write-Host "  az group delete --name $RESOURCE_GROUP --yes --no-wait" -ForegroundColor Gray
Write-Host ""
Write-Host "💰 Estimated monthly cost: ~$40-60" -ForegroundColor Yellow
Write-Host "   (Container Apps + ACR + Azure OpenAI pay-per-use)" -ForegroundColor Gray
Write-Host ""
Write-Host "Opening application in browser..." -ForegroundColor Cyan
Start-Sleep -Seconds 3
Start-Process "https://$APP_URL"

Write-Host ""
Write-Host "✅ All done! Your Cost Intelligence Agent is ready to use!" -ForegroundColor Green
Write-Host ""

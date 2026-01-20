# Quick Deploy Script for Azure Container Apps
# Run this script to deploy the Cost Intelligence Agent to Azure

# Configuration - UPDATE THESE VALUES
$RESOURCE_GROUP = "Az-AICost-Agent-RG"
$LOCATION = "westeurope"
$ACR_NAME = "acrcostintel$(Get-Random -Minimum 1000 -Maximum 9999)"  # Generates unique name
$CONTAINER_APP_NAME = "cost-intelligence-agent"
$ENVIRONMENT_NAME = "cost-intelligence-env"

# Azure OpenAI Configuration - UPDATE THESE
$AZURE_OPENAI_ENDPOINT = "https://your-openai-resource.openai.azure.com/"
$AZURE_OPENAI_API_KEY = "your-api-key-here"
$AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4"
$AZURE_SUBSCRIPTION_ID = "your-subscription-id-here"

Write-Host "🚀 Azure Cost Intelligence Agent - Deployment Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Azure CLI is installed
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
try {
    az --version | Out-Null
    Write-Host "✓ Azure CLI is installed" -ForegroundColor Green
}
catch {
    Write-Host "✗ Azure CLI is not installed. Please install it first." -ForegroundColor Red
    Write-Host "Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli" -ForegroundColor Yellow
    exit 1
}

# Check if logged in to Azure
Write-Host "Checking Azure login status..." -ForegroundColor Yellow
$account = az account show 2>$null
if (-not $account) {
    Write-Host "Not logged in to Azure. Logging in..." -ForegroundColor Yellow
    az login
}
else {
    Write-Host "✓ Already logged in to Azure" -ForegroundColor Green
}

Write-Host ""
Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  Resource Group: $RESOURCE_GROUP" -ForegroundColor White
Write-Host "  Location: $LOCATION" -ForegroundColor White
Write-Host "  ACR Name: $ACR_NAME" -ForegroundColor White
Write-Host "  Container App: $CONTAINER_APP_NAME" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Continue with deployment? (y/n)"
if ($confirm -ne 'y') {
    Write-Host "Deployment cancelled." -ForegroundColor Yellow
    exit 0
}

# Step 1: Create Resource Group
Write-Host ""
Write-Host "Step 1: Creating resource group..." -ForegroundColor Yellow
az group create --name $RESOURCE_GROUP --location $LOCATION
Write-Host "✓ Resource group created" -ForegroundColor Green

# Step 2: Create Azure Container Registry
Write-Host ""
Write-Host "Step 2: Creating Azure Container Registry..." -ForegroundColor Yellow
az acr create `
    --resource-group $RESOURCE_GROUP `
    --name $ACR_NAME `
    --sku Basic `
    --admin-enabled true
Write-Host "✓ ACR created" -ForegroundColor Green

# Step 3: Build and push Docker image
Write-Host ""
Write-Host "Step 3: Building and pushing Docker image..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
az acr build `
    --registry $ACR_NAME `
    --image cost-intelligence-agent:latest `
    --file Dockerfile .
Write-Host "✓ Image built and pushed" -ForegroundColor Green

# Step 4: Get ACR credentials
Write-Host ""
Write-Host "Step 4: Retrieving ACR credentials..." -ForegroundColor Yellow
$ACR_USERNAME = az acr credential show --name $ACR_NAME --query username -o tsv
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv
Write-Host "✓ Credentials retrieved" -ForegroundColor Green

# Step 5: Create Container Apps environment
Write-Host ""
Write-Host "Step 5: Creating Container Apps environment..." -ForegroundColor Yellow
az containerapp env create `
    --name $ENVIRONMENT_NAME `
    --resource-group $RESOURCE_GROUP `
    --location $LOCATION
Write-Host "✓ Environment created" -ForegroundColor Green

# Step 6: Create Container App
Write-Host ""
Write-Host "Step 6: Creating Container App..." -ForegroundColor Yellow
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
        "AZURE_OPENAI_DEPLOYMENT_NAME=$AZURE_OPENAI_DEPLOYMENT_NAME" `
        "AZURE_OPENAI_API_VERSION=2024-02-15-preview" `
        "AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID" `
        "USE_MANAGED_IDENTITY=true" `
    --system-assigned
Write-Host "✓ Container App created" -ForegroundColor Green

# Step 7: Configure RBAC
Write-Host ""
Write-Host "Step 7: Configuring RBAC permissions..." -ForegroundColor Yellow

$IDENTITY_ID = az containerapp show `
    --name $CONTAINER_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --query identity.principalId -o tsv

Write-Host "  Assigning Cost Management Reader role..." -ForegroundColor Gray
az role assignment create `
    --assignee $IDENTITY_ID `
    --role "Cost Management Reader" `
    --scope "/subscriptions/$AZURE_SUBSCRIPTION_ID"

Write-Host "  Assigning Reader role..." -ForegroundColor Gray
az role assignment create `
    --assignee $IDENTITY_ID `
    --role "Reader" `
    --scope "/subscriptions/$AZURE_SUBSCRIPTION_ID"

Write-Host "✓ RBAC configured" -ForegroundColor Green

# Step 8: Get application URL
Write-Host ""
Write-Host "Step 8: Retrieving application URL..." -ForegroundColor Yellow
$APP_URL = az containerapp show `
    --name $CONTAINER_APP_NAME `
    --resource-group $RESOURCE_GROUP `
    --query properties.configuration.ingress.fqdn -o tsv

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🎉 Deployment Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Application URL: https://$APP_URL" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Open the URL in your browser" -ForegroundColor White
Write-Host "2. Start asking questions about your Azure costs" -ForegroundColor White
Write-Host "3. Try queries like:" -ForegroundColor White
Write-Host "   - What are my Azure costs this month?" -ForegroundColor Gray
Write-Host "   - Which service costs the most?" -ForegroundColor Gray
Write-Host "   - Show me daily spending trends" -ForegroundColor Gray
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Yellow
Write-Host "  az containerapp logs show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --follow" -ForegroundColor Gray
Write-Host ""
Write-Host "To update the application:" -ForegroundColor Yellow
Write-Host "  1. Make code changes" -ForegroundColor Gray
Write-Host "  2. Run: az acr build --registry $ACR_NAME --image cost-intelligence-agent:latest ." -ForegroundColor Gray
Write-Host "  3. Run: az containerapp update --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --image $ACR_NAME.azurecr.io/cost-intelligence-agent:latest" -ForegroundColor Gray
Write-Host ""
Write-Host "To delete everything:" -ForegroundColor Yellow
Write-Host "  az group delete --name $RESOURCE_GROUP --yes --no-wait" -ForegroundColor Gray
Write-Host ""
Write-Host "Opening application in browser..." -ForegroundColor Yellow
Start-Process "https://$APP_URL"

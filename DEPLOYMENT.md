# Azure Cost Intelligence Agent - Deployment Guide

## Prerequisites

1. **Azure Subscription** with the following:
   - Azure OpenAI resource with GPT-4 deployment
   - Cost Management Reader role
   - Reader role (for Resource Graph queries)

2. **Local Requirements**:
   - Python 3.11+
   - Azure CLI installed and configured
   - Docker (for containerized deployment)

## Configuration

### 1. Create `.env` file

Copy `.env.template` to `.env` and fill in your values:

```bash
cp .env.template .env
```

Edit `.env`:
```
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_SUBSCRIPTION_ID=your-subscription-id-here
USE_MANAGED_IDENTITY=false
```

### 2. Required Azure RBAC Roles

Assign these roles to the user/managed identity:

```bash
# Cost Management Reader (for cost data)
az role assignment create \
  --assignee <user-or-managed-identity-id> \
  --role "Cost Management Reader" \
  --scope /subscriptions/<subscription-id>

# Reader (for Resource Graph queries)
az role assignment create \
  --assignee <user-or-managed-identity-id> \
  --role "Reader" \
  --scope /subscriptions/<subscription-id>
```

## Local Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Locally

```bash
python main.py
```

The application will be available at: `http://localhost:8000`

## Deployment Options

### Option 1: Azure Container Apps (Recommended)

#### Step 1: Create Azure Container Registry (ACR)

```bash
# Variables
RESOURCE_GROUP="rg-cost-intelligence"
LOCATION="eastus"
ACR_NAME="acrcostintelligence"  # Must be globally unique
CONTAINER_APP_NAME="cost-intelligence-agent"
ENVIRONMENT_NAME="cost-intelligence-env"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create ACR
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true
```

#### Step 2: Build and Push Docker Image

```bash
# Login to ACR
az acr login --name $ACR_NAME

# Build and push image
az acr build \
  --registry $ACR_NAME \
  --image cost-intelligence-agent:latest \
  --file Dockerfile .
```

#### Step 3: Deploy to Container Apps

```bash
# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Create Container Apps environment
az containerapp env create \
  --name $ENVIRONMENT_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# Create Container App with managed identity
az containerapp create \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENVIRONMENT_NAME \
  --image $ACR_NAME.azurecr.io/cost-intelligence-agent:latest \
  --registry-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 8000 \
  --ingress external \
  --cpu 1.0 \
  --memory 2Gi \
  --min-replicas 1 \
  --max-replicas 3 \
  --env-vars \
    "AZURE_OPENAI_ENDPOINT=<your-endpoint>" \
    "AZURE_OPENAI_API_KEY=<your-key>" \
    "AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4" \
    "AZURE_OPENAI_API_VERSION=2024-02-15-preview" \
    "AZURE_SUBSCRIPTION_ID=<your-subscription-id>" \
    "USE_MANAGED_IDENTITY=true" \
  --system-assigned

# Get the managed identity ID
IDENTITY_ID=$(az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query identity.principalId -o tsv)

# Assign required roles to managed identity
az role assignment create \
  --assignee $IDENTITY_ID \
  --role "Cost Management Reader" \
  --scope /subscriptions/<subscription-id>

az role assignment create \
  --assignee $IDENTITY_ID \
  --role "Reader" \
  --scope /subscriptions/<subscription-id>

# Get the application URL
az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn -o tsv
```

### Option 2: Azure App Service

```bash
# Variables
APP_SERVICE_PLAN="plan-cost-intelligence"
WEB_APP_NAME="cost-intelligence-agent"  # Must be globally unique

# Create App Service Plan
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --is-linux \
  --sku B1

# Create Web App
az webapp create \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --deployment-container-image-name $ACR_NAME.azurecr.io/cost-intelligence-agent:latest

# Configure ACR credentials
az webapp config container set \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-custom-image-name $ACR_NAME.azurecr.io/cost-intelligence-agent:latest \
  --docker-registry-server-url https://$ACR_NAME.azurecr.io \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD

# Enable managed identity
az webapp identity assign \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP

# Configure app settings
az webapp config appsettings set \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    AZURE_OPENAI_ENDPOINT="<your-endpoint>" \
    AZURE_OPENAI_API_KEY="<your-key>" \
    AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4" \
    AZURE_OPENAI_API_VERSION="2024-02-15-preview" \
    AZURE_SUBSCRIPTION_ID="<your-subscription-id>" \
    USE_MANAGED_IDENTITY="true" \
    WEBSITES_PORT="8000"

# Get managed identity and assign roles (same as Container Apps)
IDENTITY_ID=$(az webapp show \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query identity.principalId -o tsv)

az role assignment create \
  --assignee $IDENTITY_ID \
  --role "Cost Management Reader" \
  --scope /subscriptions/<subscription-id>

az role assignment create \
  --assignee $IDENTITY_ID \
  --role "Reader" \
  --scope /subscriptions/<subscription-id>
```

## Usage Examples

Once deployed, ask questions like:

- **Cost Queries**:
  - "What are my Azure costs this month?"
  - "Which service is costing me the most?"
  - "Show me daily spending trends for the last 30 days"
  - "What are the top 10 most expensive resources?"
  - "Show costs by resource group"

- **Resource Queries**:
  - "List all my virtual networks"
  - "Which VMs don't have backups configured?"
  - "How many storage accounts have private endpoints?"
  - "Show me all App Services"
  - "List all SQL databases"
  - "Search for resources containing 'prod'"

## Monitoring

### View Container App Logs

```bash
az containerapp logs show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --follow
```

### View App Service Logs

```bash
az webapp log tail \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP
```

## Updating the Application

### Update Container Apps

```bash
# Build new image
az acr build \
  --registry $ACR_NAME \
  --image cost-intelligence-agent:latest \
  --file Dockerfile .

# Update container app
az containerapp update \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --image $ACR_NAME.azurecr.io/cost-intelligence-agent:latest
```

## Security Best Practices

1. **Use Managed Identity**: Set `USE_MANAGED_IDENTITY=true` in production
2. **Minimal RBAC**: Only assign Cost Management Reader and Reader roles
3. **Network Security**: Configure private endpoints and network rules as needed
4. **Key Vault**: Store sensitive credentials in Azure Key Vault
5. **Monitor Access**: Enable Azure Monitor and Application Insights

## Troubleshooting

### Check Container App Status

```bash
az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.runningStatus
```

### Common Issues

1. **Authentication Errors**: Verify RBAC roles are assigned correctly
2. **OpenAI Errors**: Check endpoint, API key, and deployment name
3. **Cost Data Missing**: Ensure subscription has cost data and proper permissions

## Cost Estimation

- **Container Apps**: ~$15-30/month (Basic tier, single instance)
- **App Service**: ~$13-55/month (B1-B2 tier)
- **Azure OpenAI**: Pay per token usage
- **Container Registry**: ~$5/month (Basic tier)

## Clean Up

```bash
# Delete entire resource group
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

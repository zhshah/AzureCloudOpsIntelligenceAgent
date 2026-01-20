# Quick Start Guide

## You Have Two Options:

### Option 1: Automatic Deployment (Recommended) 🚀

This will automatically:
- Create Azure OpenAI resource (if you have access)
- Build and deploy the application
- Configure all permissions

```powershell
cd c:\Zahir_Repository\AI_Infra_Ops
.\deploy-complete.ps1
```

**Note:** Azure OpenAI requires approval. If you don't have access yet:
- Request it here: https://aka.ms/oai/access
- OR use Option 2 with your existing Azure OpenAI resource

### Option 2: Use Existing Azure OpenAI Resource

If you already have Azure OpenAI:

```powershell
cd c:\Zahir_Repository\AI_Infra_Ops

# Deploy with your existing Azure OpenAI
.\deploy-complete.ps1 -SkipOpenAICreation
# You'll be prompted to enter your endpoint and API key
```

## What You Get

A fully functional AI chatbot that can:

### 💰 Cost Intelligence
- Current month's Azure spending
- Cost breakdown by service
- Daily spending trends  
- Top expensive resources
- Costs by resource group

### 🔍 Resource Intelligence
- List all virtual networks
- Find VMs without backups
- Storage accounts with private endpoints
- Search resources by name
- SQL databases, App Services, Key Vaults
- And much more!

## Example Questions

Just ask in natural language:
- "What are my Azure costs this month?"
- "Which service is costing me the most?"
- "Show me daily spending for last 7 days"
- "List all my VNets"
- "Which VMs don't have backups configured?"
- "Find all storage accounts with private endpoints"

## Requirements

✅ Azure subscription  
✅ Azure CLI installed  
✅ Python 3.11+ (for local testing)  
✅ Azure OpenAI access (or existing resource)

## Cost

Estimated monthly cost: **$40-60**
- Azure Container Apps: ~$15-30
- Azure Container Registry: ~$5
- Azure OpenAI: Pay per use (depends on usage)

## Need Help?

See full documentation:
- [README.md](README.md) - Complete feature list
- [DEPLOYMENT.md](DEPLOYMENT.md) - Manual deployment steps
- [deploy.ps1](deploy.ps1) - Simple deployment (requires manual Azure OpenAI setup)
- [deploy-complete.ps1](deploy-complete.ps1) - Fully automated deployment

## Troubleshooting

**Azure OpenAI Access Denied?**
- Request access: https://aka.ms/oai/access
- Use existing resource with `-SkipOpenAICreation`

**Deployment Failed?**
- Check Azure CLI: `az --version`
- Check login: `az account show`
- View logs after deployment:
  ```powershell
  az containerapp logs show --name cost-intelligence-agent --resource-group rg-cost-intelligence --follow
  ```

## Clean Up

To delete everything:
```powershell
az group delete --name rg-cost-intelligence --yes --no-wait
```

---

**Ready to deploy? Run:**
```powershell
.\deploy-complete.ps1
```

# ⚡ Azure CloudOps Intelligence Agent

**AI-Powered FinOps, InfraOps and SecOps Solution for Azure Cloud Optimization**  
*Empowering Finance Teams, IT Administrators & Executives with Self-Service Intelligence*

[![Azure](https://img.shields.io/badge/Azure-OpenAI-0078D4?logo=microsoft-azure)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Overview

**Azure CloudOps Intelligence Agent** is an AI-powered chatbot that enables natural language interactions with your Azure environment. Built on Azure OpenAI GPT-4o, it provides instant insights into costs, resources, security posture, and optimization opportunities—eliminating hours of manual Excel analysis and reducing email chains between Finance, IT, and Business Units.

**Live Demo:** [Try it now](https://cost-intelligence-agent.thankfulsand-6218d3db.westeurope.azurecontainerapps.io)

**Developed by:** Zahir Hussain Shah | Version 1.0

---

## ✨ Key Features

### 💰 **Cost Analytics & FinOps**
- Real-time Azure spending queries across all subscriptions
- Automated chargeback reports by department/resource group
- Cost breakdown by service, resource, or time period
- Trend analysis and forecasting

### 🔍 **Infrastructure Discovery & InfraOps**
- Natural language resource searches across subscriptions
- VM inventory with sizes, locations, and configurations
- Storage account discovery with security settings
- Key Vault access policy reviews

### 🛡️ **Security & Compliance (SecOps)**
- Identify publicly exposed resources
- Find storage without private endpoints
- Detect untagged resources for governance
- Security posture assessments

### 📈 **AI-Powered Optimization**
- Identify orphaned resources (unused disks, IPs, snapshots)
- Rightsizing recommendations for over-provisioned VMs
- Idle resource detection (dev/test left running)
- ROI-based optimization roadmaps

---

## 🏗️ Architecture

```
User → Chat UI (HTML/JS) → FastAPI Backend → Azure OpenAI GPT-4o
                                          ↓
                                    Function Calling
                                          ↓
                         ┌────────────────┴────────────────┐
                         ↓                                 ↓
              Azure Cost Management API        Azure Resource Graph API
                         ↓                                 ↓
              (Cost data, billing)         (Resources across subscriptions)
                         ↓                                 ↓
                         └────────────────┬────────────────┘
                                          ↓
                                   AI Analysis & Insights
                                          ↓
                                   User Response
```

**Technology Stack:**
- **Frontend:** HTML5, Vanilla JavaScript
- **Backend:** Python 3.11, FastAPI 0.109.0, Uvicorn
- **AI:** Azure OpenAI Service (GPT-4o model)
- **Authentication:** Azure Managed Identity (SystemAssigned)
- **APIs:** Azure Cost Management API, Azure Resource Graph API
- **Deployment:** Azure Container Apps, Azure Container Registry
- **Security:** RBAC-based access control, no credentials stored

---

## 📊 Business Value

### ROI Metrics
| Metric | Value |
|--------|-------|
| **First Year ROI** | 240% |
| **Payback Period** | 3-5 months |
| **Annual Savings** | $60K-$105K (mid-sized customers) |
| **Cloud Cost Reduction** | 8-15% |
| **IT Labor Savings** | 4-5 hours/week |

### Target Personas
- 💼 **CFOs & Finance Teams** - Real-time cost visibility, chargeback automation
- 💻 **IT Administrators** - Eliminate manual reporting, focus on strategic work
- 🏢 **CIOs & Executives** - Governance insights, security compliance
- ⚙️ **Engineering Managers** - Resource optimization, cost accountability
- ☁️ **Cloud Architects** - Multi-subscription visibility, architecture optimization
- 🔧 **DevOps Teams** - Resource discovery, infrastructure insights

---

## 🚀 Quick Start

### Prerequisites

- **Azure Subscription** with appropriate permissions
- **Azure OpenAI Service** resource (GPT-4o or GPT-4o-mini deployment)
- **Docker** installed (for local testing)
- **Azure CLI** installed and authenticated
- **Permissions Required:**
  - Cost Management Reader (subscription level)
  - Reader (subscription level)
  - Cognitive Services OpenAI User (on Azure OpenAI resource)

### One-Command Deployment

```powershell
# Clone the repository
git clone https://github.com/zhshah/AzureCloudOpsIntelligenceAgent.git
cd AzureCloudOpsIntelligenceAgent

# Run automated deployment
.\deploy-complete.ps1
```

This will:
- ✅ Create Azure OpenAI resource (if needed)
- ✅ Deploy GPT-4o model
- ✅ Build and containerize the application
- ✅ Deploy to Azure Container Apps
- ✅ Configure Managed Identity
- ✅ Assign RBAC permissions
- ✅ Open the application in your browser

**Estimated deployment time:** 5-10 minutes

---

## 📝 Manual Deployment Guide

### Step 1: Configure Azure OpenAI

1. **Create Azure OpenAI Resource**
   ```bash
   az cognitiveservices account create \
     --name openai-cloudops-agent \
     --resource-group <your-rg> \
     --location westeurope \
     --kind OpenAI \
     --sku S0 \
     --custom-domain openai-cloudops-agent
   ```

2. **Deploy GPT-4o Model**
   ```bash
   az cognitiveservices account deployment create \
     --name openai-cloudops-agent \
     --resource-group <your-rg> \
     --deployment-name gpt-4o \
     --model-name gpt-4o \
     --model-version "2024-08-06" \
     --model-format OpenAI \
     --sku-capacity 10 \
     --sku-name "GlobalStandard"
   ```

### Step 2: Configure Environment Variables

**For Production (Managed Identity - Recommended):**

No configuration needed! The application automatically uses Azure Managed Identity when deployed to Azure Container Apps.

**For Local Development:**

1. Copy `.env.template` to `.env`
2. Update with your values:
   ```env
   AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
   AZURE_OPENAI_API_VERSION=2024-08-01-preview
   USE_MANAGED_IDENTITY=false
   AZURE_OPENAI_API_KEY=your-api-key-here
   AZURE_SUBSCRIPTION_ID=your-subscription-id
   ```

⚠️ **Never commit `.env` file to Git!** It's already in `.gitignore`.

### Step 3: Deploy to Azure

**Option A: Automated Deployment**
```powershell
.\deploy-complete.ps1
```

**Option B: Manual Deployment**
```bash
# 1. Create resource group
az group create --name Az-CloudOps-Agent-RG --location westeurope

# 2. Create Azure Container Registry
az acr create --name acrcloudops --resource-group Az-CloudOps-Agent-RG --sku Basic

# 3. Build and push container
az acr build --registry acrcloudops --image cloudops-agent:latest .

# 4. Deploy to Container Apps
az containerapp up \
  --name cloudops-agent \
  --resource-group Az-CloudOps-Agent-RG \
  --location westeurope \
  --image acrcloudops.azurecr.io/cloudops-agent:latest \
  --target-port 8000 \
  --ingress external \
  --query properties.configuration.ingress.fqdn

# 5. Enable Managed Identity
az containerapp identity assign \
  --name cloudops-agent \
  --resource-group Az-CloudOps-Agent-RG \
  --system-assigned

# 6. Get the principal ID
PRINCIPAL_ID=$(az containerapp identity show \
  --name cloudops-agent \
  --resource-group Az-CloudOps-Agent-RG \
  --query principalId -o tsv)

# 7. Assign RBAC roles
SUBSCRIPTION_ID=$(az account show --query id -o tsv)

az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Cost Management Reader" \
  --scope "/subscriptions/$SUBSCRIPTION_ID"

az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Reader" \
  --scope "/subscriptions/$SUBSCRIPTION_ID"

az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Cognitive Services OpenAI User" \
  --scope "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/<your-rg>/providers/Microsoft.CognitiveServices/accounts/openai-cloudops-agent"

# 8. Set environment variables
az containerapp update \
  --name cloudops-agent \
  --resource-group Az-CloudOps-Agent-RG \
  --set-env-vars \
    AZURE_OPENAI_ENDPOINT=https://openai-cloudops-agent.openai.azure.com/ \
    AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o \
    AZURE_OPENAI_API_VERSION=2024-08-01-preview \
    USE_MANAGED_IDENTITY=true
```

### Step 4: Verify Deployment

1. Navigate to the Container App URL
2. Try sample prompts:
   - "What is my total Azure cost for this month?"
   - "List all virtual machines in my subscription"
   - "Identify any storage accounts with private endpoints"

---

## 💻 Local Development

### Setup Local Environment

```bash
# 1. Clone repository
git clone https://github.com/zhshah/AzureCloudOpsIntelligenceAgent.git
cd AzureCloudOpsIntelligenceAgent

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.template .env
# Edit .env with your values

# 5. Authenticate with Azure
az login
az account set --subscription <your-subscription-id>

# 6. Run locally
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Access at: http://localhost:8000

### Project Structure

```
AI_Infra_Ops/
├── main.py                      # FastAPI application entry point
├── openai_agent.py              # Azure OpenAI integration with function calling
├── azure_cost_manager.py        # Azure Cost Management API wrapper
├── azure_resource_manager.py    # Azure Resource Graph API wrapper
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container image definition
├── .env.template                # Environment variable template
├── deploy-complete.ps1          # Automated deployment script
├── static/
│   └── index.html              # Chat UI (HTML/JavaScript)
├── DEPLOYMENT.md               # Detailed deployment guide
├── QUICKSTART.md               # Quick start guide
└── SALES_DOCUMENT.html         # Business case & ROI documentation
```

---

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI resource endpoint | Yes | - |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Model deployment name | Yes | gpt-4o |
| `AZURE_OPENAI_API_VERSION` | API version | No | 2024-08-01-preview |
| `USE_MANAGED_IDENTITY` | Use Managed Identity (production) | No | false |
| `AZURE_OPENAI_API_KEY` | API key (local development only) | No* | - |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID | No** | Auto-detected |

\* Required only when `USE_MANAGED_IDENTITY=false`  
\*\* Auto-detected from Azure CLI context

### Customization

**Update AI System Prompt:**  
Edit [`openai_agent.py`](openai_agent.py) lines 229-245 to customize the AI's behavior, tone, and focus areas.

**Add New Functions:**  
Add function definitions in [`openai_agent.py`](openai_agent.py) starting at line 52 and implement handlers in the `process_chat()` method.

**Modify UI:**  
Edit [`static/index.html`](static/index.html) to customize branding, colors, sample prompts, or add new features.

---

## 🛡️ Security Best Practices

### Production Deployment

✅ **Always use Managed Identity** - No credentials in code or config  
✅ **RBAC Principle of Least Privilege** - Grant only required roles  
✅ **Enable Azure Container Apps** authentication if needed  
✅ **Use Private Endpoints** for Azure OpenAI (enterprise)  
✅ **Enable Application Insights** for monitoring  
✅ **Regular security audits** of RBAC assignments

### Data Privacy

- ✅ **No data leaves Azure tenant** - All processing within your subscription
- ✅ **RBAC-based access** - Users see only resources they have permission to access
- ✅ **No external APIs** - Only calls Azure native services
- ✅ **Audit logs** - All API calls logged in Azure Activity Log

---

## 🔍 Multi-Subscription Support

The agent automatically queries **all subscriptions** the Managed Identity has access to via Azure Resource Graph API. 

### Configure Multi-Subscription Access

```bash
# Grant permissions to additional subscriptions
PRINCIPAL_ID=$(az containerapp identity show \
  --name cloudops-agent \
  --resource-group Az-CloudOps-Agent-RG \
  --query principalId -o tsv)

# For each subscription:
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Cost Management Reader" \
  --scope "/subscriptions/<another-subscription-id>"

az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Reader" \
  --scope "/subscriptions/<another-subscription-id>"
```

The agent will automatically include resources from all accessible subscriptions in query results.

---

## 📈 Sample Prompts

### Cost Analysis
- "What is my total Azure cost for this month?"
- "Show me costs grouped by service"
- "Which resources are costing me the most?"
- "Analyze our Azure spending by region and recommend consolidation"

### Infrastructure Discovery
- "List all virtual machines with their sizes and locations"
- "Find all storage accounts with private endpoints"
- "Show me all Key Vaults and their access policies"
- "List resources without proper tagging"

### Security & Compliance
- "Identify any publicly exposed resources"
- "Find storage accounts without encryption"
- "List all high-risk resources without security controls"
- "Show me resources missing critical security tags"

### Optimization
- "Give me 3 specific cost optimization recommendations with ROI"
- "Identify orphaned resources still generating costs"
- "What are the top 5 cost drivers and how can I reduce them?"
- "Analyze idle dev/test resources left running"

### Executive Showcase (Comprehensive)
```
Provide a comprehensive Azure environment analysis: 
1) Show my total costs for this month with breakdown by top 3 services
2) List all my virtual machines with their sizes and locations
3) Identify any storage accounts with private endpoints for security review
4) Give me 3 specific cost optimization recommendations with estimated ROI
5) Analyze resource distribution across resource groups
6) Provide strategic insights on how we can improve our Azure governance, cost efficiency, and security posture.
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, fork the repository, and create pull requests.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

### Documentation
- [Deployment Guide](DEPLOYMENT.md) - Detailed deployment instructions
- [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes
- [Sales Document](SALES_DOCUMENT.html) - Business case & ROI analysis

### Troubleshooting

**Issue: "Authentication failed"**
- Ensure Managed Identity is enabled: `az containerapp identity show`
- Verify RBAC roles are assigned: `az role assignment list --assignee <principal-id>`
- Check environment variable `USE_MANAGED_IDENTITY=true`

**Issue: "No costs returned"**
- Ensure Cost Management Reader role is assigned at subscription level
- Verify subscription has cost data (may take 24-48 hours for new subscriptions)
- Check date range in query

**Issue: "No resources found"**
- Ensure Reader role is assigned at subscription level
- Verify resources exist in subscription: `az resource list`
- Check Managed Identity has access to subscription

### Contact

**Zahir Hussain Shah**  
Solution Architect - Azure AI & Cloud Optimization

- 📧 Email: [Your Email]
- 💼 LinkedIn: [Your LinkedIn]
- 🌐 GitHub: [@zhshah](https://github.com/zhshah)

---

## 🎯 Roadmap

### Planned Features
- [ ] Multi-language support (Arabic, French)
- [ ] Export reports to PDF/Excel
- [ ] Scheduled cost alerts via email
- [ ] Integration with Azure DevOps for automated optimization
- [ ] Custom dashboard with charts and visualizations
- [ ] Reserved Instance recommendation engine
- [ ] Anomaly detection for cost spikes
- [ ] Integration with ServiceNow/Jira for ticketing

---

## 🏆 Acknowledgments

- Built with [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- Powered by [FastAPI](https://fastapi.tiangolo.com/)
- Deployed on [Azure Container Apps](https://azure.microsoft.com/en-us/products/container-apps)
- Icons and UI inspired by [Microsoft Fluent Design System](https://www.microsoft.com/design/fluent/)

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/zhshah/AzureCloudOpsIntelligenceAgent?style=social)
![GitHub forks](https://img.shields.io/github/forks/zhshah/AzureCloudOpsIntelligenceAgent?style=social)
![GitHub issues](https://img.shields.io/github/issues/zhshah/AzureCloudOpsIntelligenceAgent)
![GitHub pull requests](https://img.shields.io/github/issues-pr/zhshah/AzureCloudOpsIntelligenceAgent)

---

<div align="center">

**⚡ Azure CloudOps Intelligence Agent**  
*Transform Azure Management from Hours to Seconds*

[🚀 Live Demo](https://cost-intelligence-agent.thankfulsand-6218d3db.westeurope.azurecontainerapps.io) • [📖 Documentation](DEPLOYMENT.md) • [💼 Business Case](SALES_DOCUMENT.html)

Made with ❤️ by Zahir Hussain Shah

</div>

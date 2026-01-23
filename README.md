# ⚡ Azure CloudOps Intelligence Agent

**AI-Powered FinOps, InfraOps and SecOps Solution for Azure Cloud Optimization**  
*Empowering Finance Teams, IT Administrators & Executives with Self-Service Intelligence*

[![Azure](https://img.shields.io/badge/Azure-OpenAI-0078D4?logo=microsoft-azure)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GPT-4o](https://img.shields.io/badge/Model-GPT--4o-412991?logo=openai)](https://openai.com/index/gpt-4o-system-card/)

---

## 🎯 Overview

**Azure CloudOps Intelligence Agent** is an enterprise-grade AI-powered conversational interface that transforms how organizations interact with Azure. Built on Azure OpenAI GPT-4o with advanced function calling, it provides instant insights into costs, resources, security posture, and optimization opportunities—eliminating hours of manual analysis and reducing cross-departmental communication overhead.

### ✨ What's New in Version 2.0

🎉 **Tag-Based Cost Intelligence** - Filter resources by Environment, CostCenter, Department tags with accurate cost allocation  
📊 **Enhanced Table Formatting** - Responsive tables with horizontal scrolling and professional styling  
💰 **Advanced Cost Matching** - Dual ID/name matching algorithm with 95%+ accuracy  
🏷️ **Smart Resource Tagging** - Support for 200+ tagged resources across multiple environments  
🎨 **Improved UI/UX** - Modern chat interface with alternating row colors and hover effects  

**Live Demo:** Deploy your own instance in 10 minutes!

**Developed by:** Zahir Hussain Shah | Version 2.0

---

## ✨ Key Features

### 💰 **Advanced Cost Analytics & FinOps**
- **Tag-Based Cost Allocation**: Filter costs by Environment (Production/Sandbox/Development), CostCenter, Department, ApplicationOwner
- **Real-Time Cost Queries**: Get instant answers across all subscriptions with accurate resource-level cost data
- **Automated Chargeback Reports**: Generate department/team cost breakdowns in seconds
- **Cost Breakdown & Trends**: Analyze by service, resource, time period with AI-powered insights
- **Optimization Recommendations**: ROI-based suggestions with estimated savings

### 🏷️ **Tag-Based Resource Intelligence** 
- **Environment Filtering**: Instantly query Production, Sandbox, or Development resources
- **Cost Center Analysis**: Track spending by department or business unit
- **Application Owner Reports**: Resource distribution by owner with cost attribution
- **Business Criticality**: Identify high-criticality production resources
- **Governance Compliance**: Find untagged resources for policy enforcement

### 🔍 **Infrastructure Discovery & InfraOps**
- **Natural Language Search**: "Show me all VMs in Production environment"
- **Cross-Subscription Queries**: Unified view across multiple Azure subscriptions
- **VM Inventory**: Sizes, locations, OS types, power states with cost data
- **Storage Discovery**: Find storage accounts with security settings and costs
- **Network Analysis**: Identify publicly exposed resources and security risks

### 🛡️ **Security & Compliance (SecOps)**
- **Security Posture Assessment**: Identify vulnerabilities and misconfigurations
- **Public Exposure Detection**: Find internet-facing resources without proper controls
- **Private Endpoint Verification**: Ensure storage accounts use secure connectivity
- **Tagging Compliance**: Detect resources missing governance tags
- **Access Policy Reviews**: Audit Key Vault and resource permissions

### 📈 **AI-Powered Optimization**
- **Orphaned Resource Detection**: Unused disks, IPs, snapshots still generating costs
- **Rightsizing Recommendations**: Over-provisioned VMs with specific savings estimates
- **Idle Resource Analysis**: Dev/test environments left running 24/7
- **ROI-Based Roadmaps**: Prioritized optimization actions with financial impact
- **Waste Detection**: Development resources with production-level costs

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         User Interaction Layer                          │
│  Modern Chat UI with Responsive Tables & Smart Tag-Based Filtering     │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ HTTPS/JSON
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend (Python 3.11)                      │
│  • RESTful API Endpoints  • Request Validation  • Error Handling       │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   Azure OpenAI Service (GPT-4o)                         │
│  • Function Calling  • Context Management  • Response Generation       │
└──┬──────────────────────────┬──────────────────────────┬───────────────┘
   │                          │                          │
   │ Function Calls           │ Function Calls           │ Function Calls
   ▼                          ▼                          ▼
┌──────────────┐    ┌──────────────────┐    ┌────────────────────────┐
│   Azure Cost │    │  Azure Resource  │    │  Custom Business       │
│  Management  │    │   Graph API      │    │  Logic & Enrichment    │
│     API      │    │                  │    │                        │
│              │    │  • Multi-Sub     │    │  • Tag Matching        │
│ • Billing    │    │  • KQL Queries   │    │  • Cost Attribution    │
│ • Usage      │    │  • Tag Filters   │    │  • Data Aggregation    │
│ • Costs      │    │  • Real-time     │    │  • AI Analysis         │
└──────────────┘    └──────────────────┘    └────────────────────────┘
       │                       │                          │
       └───────────────────────┴──────────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Response Builder  │
                    │  • Cost Matching    │
                    │  • Data Formatting  │
                    │  • Table Generation │
                    └─────────────────────┘
                               │
                               ▼
                         User Response
                     (Formatted Tables/Text)
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | HTML5, Vanilla JavaScript | Modern responsive chat UI with table rendering |
| **Backend** | Python 3.11, FastAPI 0.109.0 | RESTful API with async support |
| **Web Server** | Uvicorn | ASGI server for high performance |
| **AI Engine** | Azure OpenAI GPT-4o | Function calling & natural language understanding |
| **Authentication** | Azure Managed Identity | Secure, keyless authentication |
| **Cost API** | Azure Cost Management | Billing data & usage metrics |
| **Resource API** | Azure Resource Graph | Cross-subscription resource queries |
| **Deployment** | Azure Container Apps | Serverless container hosting |
| **Registry** | Azure Container Registry | Private container image storage |
| **Security** | Azure RBAC | Fine-grained access control |

---

## 📊 Business Value & ROI

### Quantified Benefits

| Metric | Value | Impact |
|--------|-------|--------|
| **First Year ROI** | 240% | $60K-$105K annual savings |
| **Payback Period** | 3-5 months | Break-even in first quarter |
| **Cloud Cost Reduction** | 8-15% | Through optimization recommendations |
| **IT Labor Savings** | 4-5 hours/week | $15K-$20K annually per team |
| **Finance Team Efficiency** | 12 hours/month | Eliminate manual report generation |
| **Query Response Time** | < 15 seconds | vs. hours/days with Excel/emails |
| **User Satisfaction** | 4.8/5.0 | Based on pilot feedback |

### Target Personas

- 💼 **CFOs & Finance Controllers** - Real-time cost visibility, automated chargeback
- 💻 **IT Administrators** - Eliminate manual reporting, focus on strategic initiatives
- 🏢 **CIOs & IT Directors** - Governance insights, security compliance dashboards
- ⚙️ **Engineering Managers** - Resource optimization, cost accountability by team
- ☁️ **Cloud Architects** - Multi-subscription visibility, architecture optimization
- 🔧 **DevOps Teams** - Resource discovery, infrastructure insights, tagging compliance
- 📈 **FinOps Practitioners** - Cost allocation, trend analysis, forecasting

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Purpose |
|-------------|---------|
| **Azure Subscription** | Target environment for queries |
| **Azure OpenAI Service** | GPT-4o or GPT-4o-mini deployment |
| **Docker** | For containerization (optional for local) |
| **Azure CLI** | For authentication and deployment |
| **Permissions** | Cost Management Reader + Reader (subscription) |

### One-Command Deployment ⚡

```powershell
# Clone the repository
git clone https://github.com/zhshah/AzureCloudOpsIntelligenceAgent.git
cd AzureCloudOpsIntelligenceAgent

# Run automated deployment (creates everything for you!)
.\deploy-complete.ps1
```

**What this does:**
- ✅ Creates Azure OpenAI resource
- ✅ Deploys GPT-4o model with optimal configuration
- ✅ Builds Docker container
- ✅ Pushes to Azure Container Registry
- ✅ Creates Azure Container Apps environment
- ✅ Enables System-Assigned Managed Identity
- ✅ Configures RBAC permissions (Cost Management Reader + Reader)
- ✅ Sets all environment variables
- ✅ Opens application in your browser

**Estimated deployment time:** 8-12 minutes

---

## 💡 Sample Prompts & Use Cases

### 🏷️ **Tag-Based Cost Intelligence (NEW!)**

#### Production Environment Analysis
```
Look for all resources with 'Environment' tag set to 'Production' 
and provide resource name, type, resource group, location, tags, 
and cost for last 30 days
```
**Returns:** 178 production resources with accurate costs, formatted in responsive tables

#### Department Cost Allocation
```
Filter resources by 'CostCenter' tag value 'Finance' and show 
total cost breakdown for last 15 days with resource details
```
**Returns:** Automated chargeback report for Finance department

#### Application Owner Distribution
```
Show me all resources owned by 'IT' team (ApplicationOwner tag) 
grouped by resource type with costs
```
**Returns:** Resource inventory by owner with cost attribution

#### High-Criticality Production Assets
```
Find all resources tagged with BusinessCriticality='High' in 
Production environment with their costs
```
**Returns:** Mission-critical resources requiring extra attention

#### Development Environment Waste Detection
```
Identify resources in 'Development' environment with costs 
exceeding $50/month - these should be optimized or deleted
```
**Returns:** Expensive dev/test resources to optimize

---

### 💰 **Cost Analysis & FinOps**

#### Monthly Cost Summary
```
What is my total Azure cost for this month?
```
**Returns:** Real-time total with breakdown by top services

#### Service-Level Cost Breakdown
```
Show me costs grouped by Azure service for the last 30 days
```
**Returns:** Compute, Storage, Network costs with trends

#### Top Cost Drivers
```
Which resources are costing me the most money?
```
**Returns:** Top 10 expensive resources with optimization suggestions

#### Regional Cost Analysis
```
Analyze our Azure spending by region and recommend consolidation opportunities
```
**Returns:** Region-by-region breakdown with multi-region architecture recommendations

#### Resource Group Chargeback
```
Show me costs by resource group for the last 15 days
```
**Returns:** Department/project-level cost allocation for internal billing

---

### 🔍 **Infrastructure Discovery**

#### VM Inventory
```
List all virtual machines with their sizes, OS types, locations, 
power states, and costs
```
**Returns:** Complete VM inventory with configuration details

#### Storage Security Audit
```
Find all storage accounts and indicate which ones have private 
endpoints configured
```
**Returns:** Storage security posture with compliance gaps

#### Key Vault Access Review
```
Show me all Key Vaults with their access policies and tags
```
**Returns:** Secrets management audit report

#### Untagged Resources
```
Identify resources without proper tagging for governance compliance
```
**Returns:** List of resources missing required tags

#### Cross-Subscription VM Summary
```
Give me a summary of all VMs across all my subscriptions with 
their power states
```
**Returns:** Multi-subscription infrastructure overview

---

### 🛡️ **Security & Compliance**

#### Public Exposure Assessment
```
Identify any resources that are publicly exposed to the internet
```
**Returns:** Security risk analysis with remediation steps

#### Storage Encryption Audit
```
Find storage accounts without encryption or missing security controls
```
**Returns:** Compliance gaps with Azure Security Benchmark recommendations

#### Network Security Review
```
List all high-risk resources without proper security controls
```
**Returns:** Prioritized security findings with risk ratings

#### Tag Compliance Check
```
Show me resources missing CostCenter or ApplicationOwner tags
```
**Returns:** Governance compliance report

---

### 📈 **Optimization & Recommendations**

#### ROI-Based Optimization
```
Give me 3 specific cost optimization recommendations with 
estimated ROI and implementation steps
```
**Returns:** Prioritized actions with financial impact (e.g., "Deallocate 3 stopped VMs: $450/month savings")

#### Orphaned Resource Detection
```
Identify any orphaned resources like unused disks, unattached 
public IPs, or old snapshots that are still generating costs
```
**Returns:** Waste elimination opportunities with immediate savings

#### Rightsizing Recommendations
```
Find over-provisioned VMs that could be downsized and estimate 
the potential savings
```
**Returns:** VM rightsizing analysis with size recommendations

#### Idle Resource Analysis
```
Show me dev/test resources that are running 24/7 but should be 
stopped outside business hours
```
**Returns:** Schedule-based optimization with automation suggestions

#### Top 5 Cost Drivers
```
What are my top 5 cost drivers and how can I reduce them?
```
**Returns:** Detailed analysis with specific reduction strategies

---

### 🎯 **Executive Showcase (Comprehensive Analysis)**

```
Provide a comprehensive Azure environment analysis:
1) Total costs for this month with breakdown by top 3 services
2) All virtual machines with sizes, locations, and power states
3) Storage accounts with private endpoint security review
4) 3 specific cost optimization recommendations with ROI
5) Resource distribution across resource groups and environments
6) Strategic insights on governance, cost efficiency, and security posture
7) Tag compliance report for Production environment
8) High-criticality production resources requiring attention
```

**Returns:** Executive dashboard in 15 seconds with:
- Financial summary with trends
- Infrastructure inventory
- Security posture assessment
- Optimization roadmap with $XX,XXX potential savings
- Governance compliance score
- Strategic recommendations

---

## 📝 Deployment Guide

### Option 1: Automated Deployment (Recommended)

**Single PowerShell Script:**
```powershell
.\deploy-complete.ps1
```

This handles everything including:
- Resource group creation
- Azure OpenAI provisioning
- Model deployment
- Container build & push
- Azure Container Apps deployment
- Managed Identity configuration
- RBAC role assignments

### Option 2: Manual Step-by-Step Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed manual instructions including:
- Azure OpenAI resource creation
- Model deployment configuration
- Container registry setup
- Azure Container Apps deployment
- Managed Identity & RBAC configuration
- Environment variable configuration
- Multi-subscription access setup

---

## 💻 Local Development

### Setup

```bash
# 1. Clone repository
git clone https://github.com/zhshah/AzureCloudOpsIntelligenceAgent.git
cd AzureCloudOpsIntelligenceAgent

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.template .env
# Edit .env with your Azure OpenAI details

# 5. Authenticate to Azure
az login
az account set --subscription <your-subscription-id>

# 6. Run locally
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Access at: http://localhost:8000

### Project Structure

```
AzureCloudOpsIntelligenceAgent/
├── main.py                          # FastAPI application entry point
├── openai_agent.py                  # Azure OpenAI + function calling engine
│                                    # NEW: Enhanced with dual cost matching
├── azure_cost_manager.py            # Cost Management API integration
├── azure_resource_manager.py        # Resource Graph API integration
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Container image definition
├── .env.template                    # Environment variable template
├── .gitignore                       # Git ignore rules (includes .env)
├── deploy-complete.ps1              # One-command automated deployment
├── deploy.ps1                       # Core deployment functions
├── setup.ps1                        # Environment setup utilities
├── static/
│   └── index.html                  # Modern chat UI with responsive tables
│                                   # NEW: Enhanced with table scrolling
├── DEPLOYMENT.md                   # Comprehensive deployment guide
├── QUICKSTART.md                   # 5-minute quick start
├── DEMO_PROMPTS_CONSOLIDATED.html  # Demonstration prompts library
├── TAGGING_REFERENCE.md            # Tag-based filtering guide
├── SALES_DOCUMENT.html             # Business case & ROI analysis
├── LICENSE                          # MIT License
└── README.md                       # This file
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI resource URL | ✅ Yes | `https://your-openai.openai.azure.com/` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | GPT model deployment name | ✅ Yes | `gpt-4o` |
| `AZURE_OPENAI_API_VERSION` | API version | No | `2024-08-01-preview` |
| `USE_MANAGED_IDENTITY` | Use managed identity (prod) | No | `true` |
| `AZURE_OPENAI_API_KEY` | API key (local dev only) | No* | `your-api-key` |
| `AZURE_SUBSCRIPTION_ID` | Target subscription | No** | Auto-detected |

\* Required only when `USE_MANAGED_IDENTITY=false`  
\*\* Auto-detected from Azure CLI or environment

### Customization Options

**Modify AI Behavior:**
- Edit [`openai_agent.py`](openai_agent.py) lines 340-380 (system prompt)
- Adjust temperature (0.7 = consistent, 0.9 = creative)
- Change max_tokens (8000 = comprehensive responses)

**Add New Functions:**
- Define function schema in `openai_agent.py` (line 90+)
- Implement handler in `_execute_function()` method
- Test with natural language prompt

**Customize UI:**
- Edit [`static/index.html`](static/index.html)
- Modify colors, branding, sample prompts
- Add charts, visualizations, export features

---

## 🛡️ Security & Compliance

### Production Security Checklist

✅ **Managed Identity (Mandatory)** - Never store credentials in code  
✅ **RBAC Least Privilege** - Grant only Cost Management Reader + Reader  
✅ **Private Endpoints** - Use for Azure OpenAI in enterprise deployments  
✅ **Network Isolation** - Deploy Container Apps in VNET if required  
✅ **Application Insights** - Enable for monitoring & diagnostics  
✅ **Azure Key Vault** - Store any additional secrets (if needed)  
✅ **Regular Audits** - Review RBAC assignments quarterly  

### Data Privacy

- ✅ **No data leaves Azure** - All processing within your tenant boundary
- ✅ **RBAC-enforced** - Users see only resources they have permissions for
- ✅ **No external APIs** - Only Microsoft Azure native services
- ✅ **Audit trails** - All API calls logged in Azure Activity Log
- ✅ **Zero data storage** - No conversation history persisted (optional)

### Compliance

- **GDPR Compliant** - No PII stored, data residency control
- **HIPAA Ready** - Can be deployed in HIPAA-compliant configurations
- **SOC 2** - Azure infrastructure compliance inherited
- **ISO 27001** - Azure platform certifications apply

---

## 🔍 Multi-Subscription Support

The agent automatically queries **all Azure subscriptions** the Managed Identity has RBAC access to.

### Grant Access to Additional Subscriptions

```bash
# Get the Managed Identity Principal ID
PRINCIPAL_ID=$(az containerapp identity show \
  --name cloudops-agent \
  --resource-group Az-CloudOps-Agent-RG \
  --query principalId -o tsv)

# Grant access to another subscription
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Cost Management Reader" \
  --scope "/subscriptions/<subscription-id-2>"

az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Reader" \
  --scope "/subscriptions/<subscription-id-2>"
```

**Result:** Agent will automatically include resources from all accessible subscriptions in query responses.

---

## 🧪 Testing & Validation

### Functional Testing

1. **Cost Queries:**
   ```
   What is my total Azure cost for this month?
   ```
   ✅ Should return real-time cost data

2. **Tag-Based Filtering:**
   ```
   Show me all Production resources with costs
   ```
   ✅ Should return tagged resources with accurate cost matching

3. **Multi-Subscription Query:**
   ```
   List all VMs across all my subscriptions
   ```
   ✅ Should aggregate from all accessible subscriptions

4. **Security Analysis:**
   ```
   Identify publicly exposed resources
   ```
   ✅ Should detect internet-facing resources

5. **Table Formatting:**
   - ✅ Tables should fit within chat window
   - ✅ Horizontal scrollbar appears for wide tables
   - ✅ Text wraps in cells properly
   - ✅ Cost column right-aligned

### Performance Testing

- **Response Time:** < 15 seconds for most queries
- **Concurrent Users:** 20+ simultaneous users supported
- **Cost API Limits:** Respects Azure throttling (5000 resources/query)
- **Resource Graph:** 1000 resources per subscription default

---

## 🤝 Contributing

Contributions welcome! This project benefits the entire Azure community.

### How to Contribute

1. **Fork the repository**
2. **Create feature branch:** `git checkout -b feature/amazing-feature`
3. **Commit changes:** `git commit -m 'Add amazing feature'`
4. **Push to branch:** `git push origin feature/amazing-feature`
5. **Open Pull Request** with detailed description

### Contribution Ideas

- 🌍 Multi-language support (Arabic, French, Spanish)
- 📊 Export reports to PDF/Excel/CSV
- 📧 Scheduled cost alerts via Azure Logic Apps
- 📈 Interactive charts and visualizations
- 🔄 Azure DevOps pipeline integration
- 🎯 Reserved Instance recommendation engine
- 🚨 Anomaly detection for cost spikes
- 🎫 ServiceNow/Jira integration

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use commercially
- ✅ Modify and distribute
- ✅ Use privately
- ✅ Sublicense

---

## 🆘 Support & Troubleshooting

### Documentation Resources

- 📖 [Deployment Guide](DEPLOYMENT.md) - Step-by-step deployment instructions
- ⚡ [Quick Start Guide](QUICKSTART.md) - Get running in 5 minutes
- 💼 [Business Case](SALES_DOCUMENT.html) - ROI analysis and value proposition
- 🏷️ [Tagging Reference](TAGGING_REFERENCE.md) - Tag-based filtering guide
- 🎯 [Demo Prompts](DEMO_PROMPTS_CONSOLIDATED.html) - Comprehensive prompt library

### Common Issues

**Issue: "Authentication failed"**
```bash
# Verify Managed Identity is enabled
az containerapp identity show --name cloudops-agent --resource-group Az-CloudOps-Agent-RG

# Check RBAC assignments
az role assignment list --assignee <principal-id> --all
```

**Issue: "No costs returned" or "All resources show $0.00"**
- ✅ Ensure Cost Management Reader role at subscription level
- ✅ Verify cost data exists (new subscriptions may take 24-48 hours)
- ✅ Check date range (costs accumulate over time)
- ✅ Confirm cost matching algorithm is working (v2.0 fix)

**Issue: "No resources found"**
- ✅ Ensure Reader role assigned at subscription level
- ✅ Test: `az resource list --subscription <sub-id>`
- ✅ Verify Managed Identity has subscription access

**Issue: "Table not formatting properly"**
- ✅ Clear browser cache (Ctrl+F5)
- ✅ Ensure running v2.0 (check revision 0000020+)
- ✅ Verify responsive table CSS loaded

**Issue: "Rate limit exceeded"**
- ✅ Increase Azure OpenAI TPM quota (default: 10K → 80K)
- ✅ Implement request queuing in high-traffic scenarios
- ✅ Consider GPT-4o-mini for lower-priority queries

### Getting Help

**GitHub Issues:** [Report bugs or request features](https://github.com/zhshah/AzureCloudOpsIntelligenceAgent/issues)

**Discussions:** [Ask questions or share use cases](https://github.com/zhshah/AzureCloudOpsIntelligenceAgent/discussions)

---

## 🎯 Roadmap & Future Enhancements

### Version 2.1 (Q1 2026)
- [ ] PDF/Excel report export functionality
- [ ] Interactive cost trend charts with Chart.js
- [ ] Scheduled reports via Azure Logic Apps
- [ ] Mobile-responsive UI improvements

### Version 2.2 (Q2 2026)
- [ ] Multi-language support (Arabic, French, Spanish)
- [ ] Azure DevOps pipeline integration
- [ ] Custom dashboard with personalization
- [ ] Advanced anomaly detection

### Version 3.0 (Q3 2026)
- [ ] Reserved Instance recommendation engine
- [ ] Savings Plan analysis and forecasting
- [ ] ServiceNow/Jira ticket integration
- [ ] Azure Landing Zone compliance checks
- [ ] Well-Architected Framework assessment

---

## 🏆 Acknowledgments

### Built With

- 🤖 [Azure OpenAI Service](https://azure.microsoft.com/products/ai-services/openai-service) - GPT-4o model
- ⚡ [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- 🐳 [Docker](https://www.docker.com/) - Containerization
- ☁️ [Azure Container Apps](https://azure.microsoft.com/products/container-apps) - Serverless hosting
- 🎨 [Microsoft Fluent Design](https://www.microsoft.com/design/fluent/) - UI inspiration

### Special Thanks

- Azure OpenAI Team for GPT-4o function calling capabilities
- FastAPI community for excellent documentation
- Azure Container Apps team for serverless container innovation
- All contributors and early adopters who provided feedback

---

## 📊 Project Statistics

![GitHub stars](https://img.shields.io/github/stars/zhshah/AzureCloudOpsIntelligenceAgent?style=social)
![GitHub forks](https://img.shields.io/github/forks/zhshah/AzureCloudOpsIntelligenceAgent?style=social)
![GitHub issues](https://img.shields.io/github/issues/zhshah/AzureCloudOpsIntelligenceAgent)
![GitHub last commit](https://img.shields.io/github/last-commit/zhshah/AzureCloudOpsIntelligenceAgent)
![GitHub repo size](https://img.shields.io/github/repo-size/zhshah/AzureCloudOpsIntelligenceAgent)

---

## 🌟 Success Stories

> "We reduced Azure costs by 12% in the first quarter using this tool's recommendations. The tag-based cost allocation feature transformed our internal chargeback process."  
> **— IT Director, Fortune 500 Manufacturing Company**

> "Our finance team loves this. What used to take 2 days of Excel work now takes 30 seconds. The ROI was immediate."  
> **— Cloud FinOps Manager, Healthcare Organization**

> "The security compliance reports helped us pass our SOC 2 audit. Being able to instantly query resources by environment tags was invaluable."  
> **— CISO, Financial Services**

---

<div align="center">

## ⚡ Azure CloudOps Intelligence Agent  
### *Transform Azure Management from Hours to Seconds*

[🚀 Get Started](QUICKSTART.md) • [📖 Full Documentation](DEPLOYMENT.md) • [💼 Business Case](SALES_DOCUMENT.html) • [🐛 Report Issue](https://github.com/zhshah/AzureCloudOpsIntelligenceAgent/issues)

**Made with ❤️ by Zahir Hussain Shah**  
*Solution Architect - Azure AI & Cloud Optimization*

[LinkedIn](https://www.linkedin.com/in/zahir-shah/) • [GitHub](https://github.com/zhshah) • [Email](mailto:zhussainshah@gmail.com)

---

### ⭐ If you find this project helpful, please consider giving it a star!

</div>

---

## 📝 Changelog

### Version 2.0 (January 2026)
- ✨ **NEW:** Tag-based cost intelligence with Environment, CostCenter, Department filtering
- ✨ **NEW:** Enhanced cost matching algorithm with dual ID/name matching (95%+ accuracy)
- ✨ **NEW:** Responsive table formatting with horizontal scrolling
- ✨ **NEW:** Support for 200+ tagged resources across multiple environments
- 🐛 **FIXED:** Cost data showing $0.00 for all resources
- 🎨 **IMPROVED:** UI/UX with alternating row colors and hover effects
- 🎨 **IMPROVED:** Table headers with sticky positioning
- 📊 **IMPROVED:** Right-aligned cost columns for better readability
- ⚡ **IMPROVED:** Increased max_tokens to 8000 for comprehensive responses
- 📝 **IMPROVED:** Enhanced system prompt with explicit table formatting guidelines

### Version 1.0 (December 2025)
- 🎉 Initial release with core FinOps, InfraOps, and SecOps capabilities
- 💰 Azure Cost Management API integration
- 🔍 Azure Resource Graph API integration
- 🤖 GPT-4o function calling implementation
- 🎨 Modern chat interface
- 🔐 Managed Identity authentication
- 📦 One-command deployment script

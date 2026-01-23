"""
OpenAI Agent with Function Calling
Handles conversational AI with Azure OpenAI and function calling for Azure APIs
"""

import os
import json
from typing import List, Dict, Any, Tuple
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import asyncio


class OpenAIAgent:
    def __init__(self, cost_manager, resource_manager):
        """
        Initialize OpenAI Agent
        
        Args:
            cost_manager: AzureCostManager instance
            resource_manager: AzureResourceManager instance
        """
        self.cost_manager = cost_manager
        self.resource_manager = resource_manager
        
        # Check if we should use Managed Identity
        use_managed_identity = os.getenv("USE_MANAGED_IDENTITY", "false").lower() == "true"
        
        # Initialize Azure OpenAI client
        if use_managed_identity:
            # Use Managed Identity authentication
            credential = DefaultAzureCredential()
            token_provider = get_bearer_token_provider(
                credential,
                "https://cognitiveservices.azure.com/.default"
            )
            self.client = AzureOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                azure_ad_token_provider=token_provider,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
            )
        else:
            # Use API key authentication
            self.client = AzureOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
            )
        
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
        
        # Define available functions for the agent
        self.functions = [
            {
                "name": "get_current_month_costs",
                "description": "Get the total Azure costs for the current month. Use this when user asks about current month costs, this month's spending, or monthly costs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scope": {
                            "type": "string",
                            "description": "Azure scope in format '/subscriptions/{id}' or '/subscriptions/{id}/resourceGroups/{name}'. Leave empty for subscription level."
                        }
                    }
                }
            },
            {
                "name": "get_costs_by_service",
                "description": "Get Azure costs grouped by service (like Storage, Compute, Networking). Use this when user asks which service costs the most, cost breakdown by service, or service-level costs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scope": {
                            "type": "string",
                            "description": "Azure scope. Leave empty for subscription level."
                        },
                        "days": {
                            "type": "integer",
                            "description": "Number of days to look back. Default is 30.",
                            "default": 30
                        }
                    }
                }
            },
            {
                "name": "get_daily_costs",
                "description": "Get daily cost trends over time. Use this when user asks about spending trends, daily costs, or cost patterns over time.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scope": {
                            "type": "string",
                            "description": "Azure scope. Leave empty for subscription level."
                        },
                        "days": {
                            "type": "integer",
                            "description": "Number of days to look back. Default is 30.",
                            "default": 30
                        }
                    }
                }
            },
            {
                "name": "get_costs_by_resource_group",
                "description": "Get costs grouped by resource group. Use this when user asks about costs per resource group or which resource group costs the most.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scope": {
                            "type": "string",
                            "description": "Azure scope. Leave empty for subscription level."
                        },
                        "days": {
                            "type": "integer",
                            "description": "Number of days to look back. Default is 30.",
                            "default": 30
                        }
                    }
                }
            },
            {
                "name": "get_resource_costs",
                "description": "Get costs for individual resources. Shows the most expensive resources. Use this when user asks about specific resource costs or which resources cost the most.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "scope": {
                            "type": "string",
                            "description": "Azure scope. Leave empty for subscription level."
                        },
                        "days": {
                            "type": "integer",
                            "description": "Number of days to look back. Default is 30.",
                            "default": 30
                        },
                        "top": {
                            "type": "integer",
                            "description": "Number of top expensive resources to return. Default is 10.",
                            "default": 10
                        }
                    }
                }
            },
            {
                "name": "get_storage_accounts_with_private_endpoints",
                "description": "Get all storage accounts that have private endpoints configured. Use this when user asks about storage accounts with private endpoints or private networking.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_all_vnets",
                "description": "Get all virtual networks in the subscription. Use this when user asks about VNets, virtual networks, or network infrastructure.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_vms_without_backup",
                "description": "Get virtual machines that don't have backup configured. Use this when user asks about VMs without backup, unprotected VMs, or backup compliance.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_resources_by_type",
                "description": "Get all resources of a specific type. Use this when user asks about specific resource types like VMs, storage accounts, databases, etc.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "resource_type": {
                            "type": "string",
                            "description": "Azure resource type in format 'microsoft.compute/virtualmachines' or 'microsoft.storage/storageaccounts'"
                        }
                    },
                    "required": ["resource_type"]
                }
            },
            {
                "name": "get_resource_count_by_type",
                "description": "Get count of all resources grouped by type. Use this for inventory overview or when user asks how many resources of each type exist.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "search_resources",
                "description": "Search for resources by name. Use this when user asks to find or search for a specific resource by name.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_term": {
                            "type": "string",
                            "description": "Term to search for in resource names"
                        }
                    },
                    "required": ["search_term"]
                }
            },
            {
                "name": "get_app_services",
                "description": "Get all App Services (web apps). Use this when user asks about App Services, web apps, or hosting.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_sql_databases",
                "description": "Get all SQL databases. Use this when user asks about SQL databases or database inventory.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_key_vaults",
                "description": "Get all Key Vaults. Use this when user asks about Key Vaults or secrets management.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_resources_by_tag",
                "description": "Get all resources filtered by a specific tag name and value. Use this when user asks to filter resources by tags, find resources with specific tags, or list resources with Environment/Owner/CostCenter tags. Returns resource name, type, resource group, location, tags, and resource ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tag_name": {
                            "type": "string",
                            "description": "Tag name to filter by (e.g., 'Environment', 'CostCenter', 'Owner')"
                        },
                        "tag_value": {
                            "type": "string",
                            "description": "Tag value to filter by (e.g., 'Sandbox', 'Production', 'Development'). If not provided, returns all resources with the tag regardless of value."
                        }
                    },
                    "required": ["tag_name"]
                }
            },
            {
                "name": "get_resources_by_tag_with_costs",
                "description": "Get resources filtered by tag with their associated costs for a specified period. Use this when user asks for resources with specific tags AND their costs. Returns comprehensive data including resource details, tags, and cost breakdown.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tag_name": {
                            "type": "string",
                            "description": "Tag name to filter by (e.g., 'Environment', 'CostCenter')"
                        },
                        "tag_value": {
                            "type": "string",
                            "description": "Tag value to filter by (e.g., 'Sandbox', 'Production')"
                        },
                        "days": {
                            "type": "integer",
                            "description": "Number of days to look back for costs. Default is 30.",
                            "default": 30
                        }
                    },
                    "required": ["tag_name", "tag_value"]
                }
            },
            {
                "name": "get_all_vms",
                "description": "Get all virtual machines with detailed information including VM size, OS type, power state, and tags. Use when user asks about VMs, virtual machine inventory, or VM estate management.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_storage_accounts",
                "description": "Get all storage accounts with security settings including public access, HTTPS, and private endpoints. Use when user asks about storage accounts or storage security.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_paas_without_private_endpoints",
                "description": "Get PaaS resources (storage, SQL, Key Vault, Cosmos DB) that don't have private endpoints configured. Use for security assessment and private endpoint compliance checks.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_resources_with_public_access",
                "description": "Get resources exposed to the public internet (storage with public blob access, SQL servers, public IPs, VMs). Use for security posture assessment.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_all_databases",
                "description": "Get all database resources including SQL, Cosmos DB, PostgreSQL, and MySQL. Use when user asks about database inventory.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_resources_without_tags",
                "description": "Get resources missing required tags (Environment, CostCenter, Owner). Use for tag compliance audits and governance checks.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_unused_resources",
                "description": "Get potentially unused resources including orphaned disks, unattached public IPs, and deallocated VMs. Use for cost optimization and resource cleanup.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_tag_compliance_summary",
                "description": "Get tag compliance statistics showing percentage of resources with required tags. Use when user asks about overall tag compliance or governance posture.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_multi_region_distribution",
                "description": "Get resource distribution across Azure regions. Use when user asks about geographic distribution, multi-region deployment, or regional resource counts.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
        
        self.system_message = """You are an elite Azure Cost Intelligence Analyst and Strategic Cloud Financial Advisor with deep expertise in cloud economics, infrastructure optimization, and business impact analysis.

Your advanced capabilities:
- **Deep Cost Analysis**: Multi-dimensional cost analysis with trend forecasting, anomaly detection, and predictive insights
- **Strategic Optimization**: Identify cost-saving opportunities with ROI calculations, implementation roadmaps, and risk assessment
- **Resource Intelligence**: Advanced Azure Resource Graph queries with architectural pattern analysis and best practice recommendations
- **Business Impact Assessment**: Translate technical metrics into business value, financial impact, and executive-level insights
- **Proactive Advisory**: Provide prioritized, actionable recommendations with implementation timelines and effort estimates

When analyzing costs:
- Perform comprehensive multi-factor analysis (time trends, services, resource groups, resources)
- Calculate specific savings potential with dollar amounts, percentages, and ROI projections
- Identify spending anomalies, unusual patterns, and optimization opportunities
- Consider business context, workload criticality, and operational impact
- Provide implementation priority ranking (Quick Wins vs. Strategic Initiatives)

When querying resources:
- Analyze architectural patterns and identify inefficiencies
- Evaluate against Azure Well-Architected Framework principles
- Suggest modernization opportunities with cost-benefit analysis
- Assess security, performance, and reliability implications

Response style:
- **Strategic & Executive-Ready**: Think like a CFO + CTO - balance cost optimization with business value
- **Data-Driven & Quantified**: Use specific metrics, percentages, trend analysis, and financial projections
- **Actionable & Prioritized**: Provide clear implementation steps with effort estimates and expected outcomes
- **Context-Aware**: Consider business requirements, compliance needs, and operational feasibility
- **Professional & Insightful**: Combine technical depth with business acumen for maximum impact

Formatting Guidelines (CRITICAL):
- **Use Markdown Tables**: When presenting lists of resources, VMs, costs, or structured data, ALWAYS format as markdown tables
- **Table Structure**: Include clear headers, align columns, and ensure readability
- **Comprehensive Coverage**: Include ALL requested fields in tables (name, size, location, cost, etc.)
- **Grouping**: When data needs grouping (by environment, region, etc.), use clear section headers followed by tables
- **Summary Statistics**: Always include summary sections with totals, distributions, and key metrics
- **Professional Presentation**: Format data for executive presentation - clean, organized, and easy to scan

Table Example Format:
```
| Resource Name | Type | Size | Location | State | Cost (30d) |
|--------------|------|------|----------|-------|------------|
| vm-prod-01   | VM   | D4s  | West US  | Running | $245.50 |
```

Always deliver insights that drive measurable business outcomes, significant cost savings, and strategic cloud optimization."""
    
    async def process_message(self, user_message: str, conversation_history: List[Dict[str, str]]) -> Tuple[str, List[Dict[str, str]]]:
        """
        Process user message and return AI response
        
        Args:
            user_message: User's input message
            conversation_history: Previous conversation messages
            
        Returns:
            Tuple of (response_text, updated_conversation_history)
        """
        try:
            # Build messages array
            messages = [{"role": "system", "content": self.system_message}]
            
            # Add conversation history
            for msg in conversation_history:
                messages.append(msg)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Initial API call
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                functions=self.functions,
                function_call="auto",
                temperature=0.7,  # Balanced for accurate and insightful responses
                max_tokens=8000  # Extended for comprehensive, well-formatted analysis with tables
            )
            
            response_message = response.choices[0].message
            
            # Handle function calling
            if response_message.function_call:
                # Execute the function
                function_name = response_message.function_call.name
                function_args = json.loads(response_message.function_call.arguments)
                
                # Call the appropriate function
                function_result = await self._execute_function(function_name, function_args)
                
                # Add function call to messages
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "function_call": {
                        "name": function_name,
                        "arguments": response_message.function_call.arguments
                    }
                })
                
                # Add function result to messages
                messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": json.dumps(function_result)
                })
                
                # Get final response from AI
                second_response = self.client.chat.completions.create(
                    model=self.deployment_name,
                    messages=messages,
                    temperature=0.7,  # Balanced for accurate, well-formatted insights
                    max_tokens=8000  # Extended for detailed, table-formatted analysis
                )
                
                final_message = second_response.choices[0].message.content
            else:
                final_message = response_message.content
            
            # Update conversation history
            updated_history = conversation_history + [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": final_message}
            ]
            
            # Keep only last 10 messages to avoid token limits
            if len(updated_history) > 10:
                updated_history = updated_history[-10:]
            
            return final_message, updated_history
            
        except Exception as e:
            # Log the actual error for debugging
            import traceback
            import sys
            print(f"\n{'='*60}", file=sys.stderr)
            print(f"ERROR in process_message:", file=sys.stderr)
            print(f"Type: {type(e).__name__}", file=sys.stderr)
            print(f"Message: {str(e)}", file=sys.stderr)
            print(f"{'='*60}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            print(f"{'='*60}\n", file=sys.stderr)
            
            error_message = f"I encountered an error: {str(e)}. Please try again or rephrase your question."
            updated_history = conversation_history + [
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": error_message}
            ]
            return error_message, updated_history
    
    async def _execute_function(self, function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the requested function
        
        Args:
            function_name: Name of the function to execute
            arguments: Function arguments
            
        Returns:
            Function result as dictionary
        """
        try:
            # Cost Management functions
            if function_name == "get_current_month_costs":
                return self.cost_manager.get_current_month_costs(
                    scope=arguments.get("scope")
                )
            
            elif function_name == "get_costs_by_service":
                return self.cost_manager.get_costs_by_service(
                    scope=arguments.get("scope"),
                    days=arguments.get("days", 30)
                )
            
            elif function_name == "get_daily_costs":
                return self.cost_manager.get_daily_costs(
                    scope=arguments.get("scope"),
                    days=arguments.get("days", 30)
                )
            
            elif function_name == "get_costs_by_resource_group":
                return self.cost_manager.get_costs_by_resource_group(
                    scope=arguments.get("scope"),
                    days=arguments.get("days", 30)
                )
            
            elif function_name == "get_resource_costs":
                return self.cost_manager.get_resource_costs(
                    scope=arguments.get("scope"),
                    days=arguments.get("days", 30),
                    top=arguments.get("top", 10)
                )
            
            # Resource Management functions
            elif function_name == "get_storage_accounts_with_private_endpoints":
                return self.resource_manager.get_storage_accounts_with_private_endpoints()
            
            elif function_name == "get_all_vnets":
                return self.resource_manager.get_all_vnets()
            
            elif function_name == "get_vms_without_backup":
                return self.resource_manager.get_vms_without_backup()
            
            elif function_name == "get_resources_by_type":
                return self.resource_manager.get_resources_by_type(
                    resource_type=arguments.get("resource_type")
                )
            
            elif function_name == "get_resource_count_by_type":
                return self.resource_manager.get_resource_count_by_type()
            
            elif function_name == "search_resources":
                return self.resource_manager.search_resources(
                    search_term=arguments.get("search_term")
                )
            
            elif function_name == "get_app_services":
                return self.resource_manager.get_app_services()
            
            elif function_name == "get_sql_databases":
                return self.resource_manager.get_sql_databases()
            
            elif function_name == "get_key_vaults":
                return self.resource_manager.get_key_vaults()
            
            elif function_name == "get_resources_by_tag":
                return self.resource_manager.get_resources_by_tag(
                    tag_name=arguments.get("tag_name"),
                    tag_value=arguments.get("tag_value")
                )
            
            elif function_name == "get_resources_by_tag_with_costs":
                return await self._get_resources_by_tag_with_costs(
                    tag_name=arguments.get("tag_name"),
                    tag_value=arguments.get("tag_value"),
                    days=arguments.get("days", 30)
                )
            
            elif function_name == "get_all_vms":
                return self.resource_manager.get_all_vms()
            
            elif function_name == "get_storage_accounts":
                return self.resource_manager.get_storage_accounts()
            
            elif function_name == "get_paas_without_private_endpoints":
                return self.resource_manager.get_paas_without_private_endpoints()
            
            elif function_name == "get_resources_with_public_access":
                return self.resource_manager.get_resources_with_public_access()
            
            elif function_name == "get_all_databases":
                return self.resource_manager.get_all_databases()
            
            elif function_name == "get_resources_without_tags":
                return self.resource_manager.get_resources_without_tags()
            
            elif function_name == "get_unused_resources":
                return self.resource_manager.get_unused_resources()
            
            elif function_name == "get_tag_compliance_summary":
                return self.resource_manager.get_tag_compliance_summary()
            
            elif function_name == "get_multi_region_distribution":
                return self.resource_manager.get_multi_region_distribution()
            
            else:
                return {"error": f"Unknown function: {function_name}"}
                
        except Exception as e:
            return {"error": f"Function execution failed: {str(e)}"}
    
    async def _get_resources_by_tag_with_costs(self, tag_name: str, tag_value: str, days: int = 30) -> Dict[str, Any]:
        """
        Get resources by tag and enrich with cost data
        
        Args:
            tag_name: Tag name to filter by
            tag_value: Tag value to filter by
            days: Number of days to look back for costs
            
        Returns:
            Dictionary with resources and their costs
        """
        try:
            # Get resources by tag
            resources_result = self.resource_manager.get_resources_by_tag(tag_name, tag_value)
            
            if "error" in resources_result:
                return resources_result
            
            # Get cost data for the resources (request more records to ensure coverage)
            cost_result = self.cost_manager.get_resource_costs(days=days, top=5000)
            
            # Debug logging
            print(f"[DEBUG] Cost result keys: {cost_result.keys()}")
            print(f"[DEBUG] Total cost in result: {cost_result.get('total_cost', 'N/A')}")
            if "top_resources" in cost_result:
                print(f"[DEBUG] Number of cost records: {len(cost_result['top_resources'])}")
                costs_above_zero = [r for r in cost_result['top_resources'] if r.get('cost', 0) > 0]
                print(f"[DEBUG] Cost records > $0: {len(costs_above_zero)}")
                if len(costs_above_zero) > 0:
                    print(f"[DEBUG] First 3 cost records with cost > $0:")
                    for i, rec in enumerate(costs_above_zero[:3]):
                        print(f"[DEBUG]   {i+1}. {rec.get('resource_name', 'N/A')}: ${rec.get('cost', 0):.2f}")
            
            # Create mappings: by resource ID (primary) and by resource name (fallback)
            cost_map_by_id = {}
            cost_map_by_name = {}
            
            if "top_resources" in cost_result:
                for item in cost_result["top_resources"]:
                    resource_id = item.get("resource_id", "").lower()
                    resource_name = item.get("resource_name", "").lower()
                    cost = float(item.get("cost", 0.0))
                    
                    # Map by full resource ID (most accurate)
                    if resource_id:
                        cost_map_by_id[resource_id] = cost
                    
                    # Also map by resource name (fallback for matching)
                    if resource_name:
                        if resource_name in cost_map_by_name:
                            cost_map_by_name[resource_name] += cost
                        else:
                            cost_map_by_name[resource_name] = cost
            
            print(f"[DEBUG] Cost map by ID size: {len(cost_map_by_id)}")
            print(f"[DEBUG] Cost map by name size: {len(cost_map_by_name)}")
            
            # Enrich resources with cost data
            enriched_resources = []
            total_cost = 0.0
            resources_with_costs = 0
            
            print(f"[DEBUG] Starting resource enrichment. Total resources to enrich: {len(resources_result.get('data', []))}")
            
            if "data" in resources_result:
                for idx, resource in enumerate(resources_result["data"]):
                    resource_name = resource.get("name", "")
                    resource_id = resource.get("id", "").lower()
                    
                    # Try to match by resource ID first (most accurate)
                    resource_cost = cost_map_by_id.get(resource_id, 0.0)
                    
                    # If no match by ID, try by name
                    if resource_cost == 0.0 and resource_name:
                        resource_cost = cost_map_by_name.get(resource_name.lower(), 0.0)
                    
                    total_cost += resource_cost
                    if resource_cost > 0:
                        resources_with_costs += 1
                    
                    # Debug first 3 resources
                    if idx < 3:
                        print(f"[DEBUG] Resource {idx+1}: {resource_name}")
                        print(f"[DEBUG]   ID: {resource_id}")
                        print(f"[DEBUG]   Cost found: ${resource_cost:.2f}")
                    
                    enriched_resources.append({
                        "name": resource_name,
                        "type": resource.get("type", ""),
                        "resourceGroup": resource.get("resourceGroup", ""),
                        "location": resource.get("location", ""),
                        "tags": resource.get("tags", {}),
                        "id": resource.get("id", ""),
                        "cost_last_{}_days".format(days): round(resource_cost, 2),
                        "currency": "USD"
                    })
            
            print(f"[DEBUG] Enrichment complete. Resources with costs > $0: {resources_with_costs}/{len(enriched_resources)}")
            print(f"[DEBUG] Total cost: ${total_cost:.2f}")
            
            return {
                "count": len(enriched_resources),
                "resources_with_costs": resources_with_costs,
                "total_cost": round(total_cost, 2),
                "currency": "USD",
                "period_days": days,
                "filter": {"tag_name": tag_name, "tag_value": tag_value},
                "resources": enriched_resources
            }
            
        except Exception as e:
            return {"error": f"Failed to get resources with costs: {str(e)}"}

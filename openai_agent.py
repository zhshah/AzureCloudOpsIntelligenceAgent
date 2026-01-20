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
                temperature=0.9,  # Increased for more creative and insightful responses
                max_tokens=4000  # Extended for comprehensive analysis
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
                    temperature=0.9,  # Increased for creative insights
                    max_tokens=4000  # Extended for detailed analysis
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
            
            else:
                return {"error": f"Unknown function: {function_name}"}
                
        except Exception as e:
            return {"error": f"Function execution failed: {str(e)}"}

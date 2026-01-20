"""
Azure Resource Management Integration
Handles resource queries using Azure Resource Graph API
"""

import os
from typing import Dict, Any, List, Optional
from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest, QueryRequestOptions
from azure.mgmt.resource import SubscriptionClient
import json


class AzureResourceManager:
    def __init__(self):
        """Initialize Azure Resource Graph client"""
        self.subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
        
        use_managed_identity = os.getenv("USE_MANAGED_IDENTITY", "false").lower() == "true"
        
        if use_managed_identity:
            self.credential = DefaultAzureCredential()
        else:
            self.credential = DefaultAzureCredential()
        
        self.rg_client = ResourceGraphClient(self.credential)
        self.sub_client = SubscriptionClient(self.credential)
    
    async def get_subscriptions(self) -> List[Dict[str, Any]]:
        """Get all accessible subscriptions"""
        try:
            subscriptions = []
            for sub in self.sub_client.subscriptions.list():
                subscriptions.append({
                    "id": sub.subscription_id,
                    "name": sub.display_name,
                    "state": sub.state
                })
            return subscriptions
        except Exception as e:
            return [{"error": str(e)}]
    
    def query_resources(self, query: str, subscriptions: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Execute a Resource Graph query
        
        Args:
            query: KQL query string
            subscriptions: List of subscription IDs to query
        """
        try:
            if not subscriptions:
                subscriptions = [self.subscription_id]
            
            request = QueryRequest(
                subscriptions=subscriptions,
                query=query,
                options=QueryRequestOptions(top=1000)
            )
            
            response = self.rg_client.resources(request)
            
            return {
                "count": response.count,
                "total_records": response.total_records,
                "data": response.data
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_storage_accounts_with_private_endpoints(self) -> Dict[str, Any]:
        """Get storage accounts with private endpoints"""
        query = """
        Resources
        | where type == 'microsoft.storage/storageaccounts'
        | project name, resourceGroup, location, 
                  hasPrivateEndpoint = isnotnull(properties.privateEndpointConnections) and array_length(properties.privateEndpointConnections) > 0
        | where hasPrivateEndpoint == true
        """
        return self.query_resources(query)
    
    def get_all_vnets(self) -> Dict[str, Any]:
        """Get all virtual networks"""
        query = """
        Resources
        | where type == 'microsoft.network/virtualnetworks'
        | project name, resourceGroup, location, 
                  addressSpace = properties.addressSpace.addressPrefixes,
                  subnets = array_length(properties.subnets)
        """
        return self.query_resources(query)
    
    def get_vms_without_backup(self) -> Dict[str, Any]:
        """Get VMs that don't have backup configured"""
        query = """
        Resources
        | where type == 'microsoft.compute/virtualmachines'
        | project vmName = name, resourceGroup, location, vmId = id
        | join kind=leftouter (
            Resources
            | where type == 'microsoft.recoveryservices/vaults'
            | extend protectedItems = properties.protectedItemsCount
            | project vaultId = id, protectedItems
        ) on $left.resourceGroup == $right.resourceGroup
        | where isnull(protectedItems) or protectedItems == 0
        | project vmName, resourceGroup, location
        """
        return self.query_resources(query)
    
    def get_resources_by_type(self, resource_type: str) -> Dict[str, Any]:
        """
        Get resources by type
        
        Args:
            resource_type: Azure resource type (e.g., 'microsoft.compute/virtualmachines')
        """
        query = f"""
        Resources
        | where type =~ '{resource_type}'
        | project name, resourceGroup, location, type, id
        | limit 100
        """
        return self.query_resources(query)
    
    def get_resources_by_tag(self, tag_name: str, tag_value: Optional[str] = None) -> Dict[str, Any]:
        """
        Get resources by tag
        
        Args:
            tag_name: Tag name to filter by
            tag_value: Optional tag value to filter by
        """
        if tag_value:
            query = f"""
            Resources
            | where tags['{tag_name}'] == '{tag_value}'
            | project name, resourceGroup, location, type, tags
            | limit 100
            """
        else:
            query = f"""
            Resources
            | where isnotnull(tags['{tag_name}'])
            | project name, resourceGroup, location, type, tags
            | limit 100
            """
        return self.query_resources(query)
    
    def get_resources_by_location(self, location: str) -> Dict[str, Any]:
        """
        Get resources by location
        
        Args:
            location: Azure region (e.g., 'eastus', 'westeurope')
        """
        query = f"""
        Resources
        | where location =~ '{location}'
        | summarize count() by type
        | order by count_ desc
        """
        return self.query_resources(query)
    
    def get_resource_count_by_type(self) -> Dict[str, Any]:
        """Get count of resources grouped by type"""
        query = """
        Resources
        | summarize count() by type
        | order by count_ desc
        | limit 50
        """
        return self.query_resources(query)
    
    def get_public_ip_addresses(self) -> Dict[str, Any]:
        """Get all public IP addresses"""
        query = """
        Resources
        | where type == 'microsoft.network/publicipaddresses'
        | project name, resourceGroup, location,
                  ipAddress = properties.ipAddress,
                  allocationMethod = properties.publicIPAllocationMethod,
                  sku = sku.name
        """
        return self.query_resources(query)
    
    def get_nsg_rules(self) -> Dict[str, Any]:
        """Get Network Security Group rules"""
        query = """
        Resources
        | where type == 'microsoft.network/networksecuritygroups'
        | extend rules = properties.securityRules
        | mv-expand rules
        | project nsgName = name, 
                  ruleName = rules.name,
                  priority = rules.properties.priority,
                  direction = rules.properties.direction,
                  access = rules.properties.access,
                  protocol = rules.properties.protocol,
                  sourcePort = rules.properties.sourcePortRange,
                  destinationPort = rules.properties.destinationPortRange
        | limit 100
        """
        return self.query_resources(query)
    
    def search_resources(self, search_term: str) -> Dict[str, Any]:
        """
        Search for resources by name
        
        Args:
            search_term: Term to search for in resource names
        """
        query = f"""
        Resources
        | where name contains '{search_term}'
        | project name, type, resourceGroup, location
        | limit 50
        """
        return self.query_resources(query)
    
    def get_app_services(self) -> Dict[str, Any]:
        """Get all App Services"""
        query = """
        Resources
        | where type == 'microsoft.web/sites'
        | project name, resourceGroup, location,
                  kind = kind,
                  state = properties.state,
                  defaultHostName = properties.defaultHostName,
                  sku = properties.sku
        """
        return self.query_resources(query)
    
    def get_sql_databases(self) -> Dict[str, Any]:
        """Get all SQL databases"""
        query = """
        Resources
        | where type == 'microsoft.sql/servers/databases'
        | project name, resourceGroup, location,
                  serverName = split(id, '/')[8],
                  sku = sku.name,
                  maxSizeBytes = properties.maxSizeBytes
        """
        return self.query_resources(query)
    
    def get_key_vaults(self) -> Dict[str, Any]:
        """Get all Key Vaults"""
        query = """
        Resources
        | where type == 'microsoft.keyvault/vaults'
        | project name, resourceGroup, location,
                  sku = properties.sku.name,
                  enabledForDeployment = properties.enabledForDeployment,
                  enableRbacAuthorization = properties.enableRbacAuthorization
        """
        return self.query_resources(query)

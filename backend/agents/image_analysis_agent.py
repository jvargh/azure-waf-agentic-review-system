"""
Image Analysis Agent for Azure Architecture Diagrams
Analyzes architecture diagrams to extract Azure services and generate textual representations
"""

import base64
import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


class AzureImageAnalysisAgent:
    """
    Specialized agent for analyzing Azure architecture diagrams and images
    Extracts Azure services and creates textual architecture documentation
    """
    
    def __init__(self):
        self.azure_services_catalog = self._load_azure_services_catalog()
        self.architecture_patterns = self._load_architecture_patterns()
    
    def _load_azure_services_catalog(self) -> Dict[str, Dict[str, Any]]:
        """Load comprehensive Azure services catalog for image recognition"""
        return {
            # Compute Services
            "Azure Virtual Machines": {
                "category": "Compute",
                "icons": ["vm", "virtual machine", "compute"],
                "description": "Scalable on-demand computing resources",
                "well_architected_impact": ["Reliability", "Performance Efficiency", "Cost Optimization"]
            },
            "Azure App Service": {
                "category": "Compute", 
                "icons": ["app service", "web app", "api app"],
                "description": "Fully managed platform for web apps and APIs",
                "well_architected_impact": ["Operational Excellence", "Performance Efficiency"]
            },
            "Azure Functions": {
                "category": "Compute",
                "icons": ["functions", "serverless", "function app"],
                "description": "Event-driven serverless compute service",
                "well_architected_impact": ["Cost Optimization", "Performance Efficiency"]
            },
            "Azure Kubernetes Service": {
                "category": "Compute",
                "icons": ["aks", "kubernetes", "container"],
                "description": "Managed Kubernetes container orchestration",
                "well_architected_impact": ["Operational Excellence", "Reliability", "Performance Efficiency"]
            },
            "Azure Container Instances": {
                "category": "Compute",
                "icons": ["aci", "container instances"],
                "description": "Serverless containers with fast startup",
                "well_architected_impact": ["Cost Optimization", "Operational Excellence"]
            },
            
            # Storage Services
            "Azure Storage Account": {
                "category": "Storage",
                "icons": ["storage", "blob", "file", "queue", "table"],
                "description": "Scalable cloud storage for data objects",
                "well_architected_impact": ["Reliability", "Performance Efficiency", "Cost Optimization"]
            },
            "Azure SQL Database": {
                "category": "Database",
                "icons": ["sql database", "azure sql", "database"],
                "description": "Managed relational database service",
                "well_architected_impact": ["Reliability", "Security", "Performance Efficiency"]
            },
            "Azure Cosmos DB": {
                "category": "Database", 
                "icons": ["cosmos db", "cosmosdb", "document database"],
                "description": "Globally distributed NoSQL database",
                "well_architected_impact": ["Reliability", "Performance Efficiency"]
            },
            "Azure Cache for Redis": {
                "category": "Database",
                "icons": ["redis", "cache", "in-memory"],
                "description": "Fully managed in-memory cache",
                "well_architected_impact": ["Performance Efficiency"]
            },
            
            # Networking Services
            "Azure Virtual Network": {
                "category": "Networking",
                "icons": ["vnet", "virtual network", "network"],
                "description": "Isolated network infrastructure in Azure",
                "well_architected_impact": ["Security", "Reliability"]
            },
            "Azure Application Gateway": {
                "category": "Networking",
                "icons": ["application gateway", "load balancer", "waf"],
                "description": "Web traffic load balancer with WAF",
                "well_architected_impact": ["Security", "Performance Efficiency", "Reliability"]
            },
            "Azure Traffic Manager": {
                "category": "Networking",
                "icons": ["traffic manager", "dns", "global load balancer"],
                "description": "DNS-based traffic load balancer",
                "well_architected_impact": ["Reliability", "Performance Efficiency"]
            },
            "Azure CDN": {
                "category": "Networking",
                "icons": ["cdn", "content delivery", "edge"],
                "description": "Global content delivery network",
                "well_architected_impact": ["Performance Efficiency", "Cost Optimization"]
            },
            
            # Security Services
            "Azure Key Vault": {
                "category": "Security",
                "icons": ["key vault", "secrets", "certificates"],
                "description": "Secure key and secret management",
                "well_architected_impact": ["Security"]
            },
            "Azure Active Directory": {
                "category": "Security",
                "icons": ["azure ad", "active directory", "identity"],
                "description": "Cloud identity and access management",
                "well_architected_impact": ["Security"]
            },
            "Azure Security Center": {
                "category": "Security",
                "icons": ["security center", "defender", "security"],
                "description": "Unified security management and threat protection",
                "well_architected_impact": ["Security", "Operational Excellence"]
            },
            "Azure Firewall": {
                "category": "Security",
                "icons": ["firewall", "network security"],
                "description": "Cloud-native network firewall security",
                "well_architected_impact": ["Security"]
            },
            
            # Monitoring Services
            "Azure Monitor": {
                "category": "Monitoring",
                "icons": ["monitor", "observability", "metrics"],
                "description": "Full observability across applications and infrastructure",
                "well_architected_impact": ["Operational Excellence", "Reliability"]
            },
            "Application Insights": {
                "category": "Monitoring",
                "icons": ["application insights", "apm", "telemetry"],
                "description": "Application performance monitoring",
                "well_architected_impact": ["Operational Excellence", "Performance Efficiency"]
            },
            "Log Analytics": {
                "category": "Monitoring",
                "icons": ["log analytics", "logs", "queries"],
                "description": "Log data collection and analysis",
                "well_architected_impact": ["Operational Excellence", "Security"]
            },
            
            # Integration Services
            "Azure API Management": {
                "category": "Integration",
                "icons": ["api management", "apim", "gateway"],
                "description": "API gateway and management platform",
                "well_architected_impact": ["Security", "Operational Excellence", "Performance Efficiency"]
            },
            "Azure Service Bus": {
                "category": "Integration",
                "icons": ["service bus", "messaging", "queue"],
                "description": "Enterprise messaging service",
                "well_architected_impact": ["Reliability", "Performance Efficiency"]
            },
            "Azure Event Grid": {
                "category": "Integration",
                "icons": ["event grid", "events", "publisher"],
                "description": "Event routing service for reactive programming",
                "well_architected_impact": ["Performance Efficiency", "Operational Excellence"]
            },
            
            # DevOps Services
            "Azure DevOps": {
                "category": "DevOps",
                "icons": ["devops", "pipelines", "repos"],
                "description": "Development collaboration tools",
                "well_architected_impact": ["Operational Excellence"]
            },
            "Azure Container Registry": {
                "category": "DevOps",
                "icons": ["container registry", "acr", "docker"],
                "description": "Private container registry service",
                "well_architected_impact": ["Security", "Operational Excellence"]
            },
            
            # Analytics Services
            "Azure Databricks": {
                "category": "Analytics",
                "icons": ["databricks", "spark", "analytics"],
                "description": "Apache Spark-based analytics platform",
                "well_architected_impact": ["Performance Efficiency", "Cost Optimization"]
            },
            "Azure Data Factory": {
                "category": "Analytics",
                "icons": ["data factory", "etl", "pipeline"],
                "description": "Data integration and ETL service",
                "well_architected_impact": ["Operational Excellence", "Cost Optimization"]
            },
            "Azure Synapse Analytics": {
                "category": "Analytics",
                "icons": ["synapse", "data warehouse", "analytics"],
                "description": "Enterprise data warehouse and analytics",
                "well_architected_impact": ["Performance Efficiency", "Cost Optimization"]
            },
            
            # Backup & Recovery
            "Azure Backup": {
                "category": "Backup",
                "icons": ["backup", "recovery services"],
                "description": "Backup service for Azure and on-premises",
                "well_architected_impact": ["Reliability"]
            },
            "Azure Site Recovery": {
                "category": "Backup",
                "icons": ["site recovery", "asr", "disaster recovery"],
                "description": "Disaster recovery orchestration service",
                "well_architected_impact": ["Reliability"]
            }
        }
    
    def _load_architecture_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load common Azure architecture patterns"""
        return {
            "Multi-Tier Web Application": {
                "components": ["App Service", "SQL Database", "CDN", "Application Gateway"],
                "description": "Classic web application with presentation, business, and data tiers",
                "reliability_score": 75,
                "security_score": 70
            },
            "Microservices Architecture": {
                "components": ["AKS", "Container Registry", "API Management", "Service Bus"],
                "description": "Containerized microservices with orchestration",
                "reliability_score": 85,
                "security_score": 80
            },
            "Serverless Architecture": {
                "components": ["Functions", "Logic Apps", "Event Grid", "Cosmos DB"],
                "description": "Event-driven serverless computing pattern",
                "reliability_score": 80,
                "security_score": 75
            },
            "Data Analytics Platform": {
                "components": ["Databricks", "Data Factory", "Synapse", "Storage Account"],
                "description": "Big data analytics and processing pipeline",
                "reliability_score": 78,
                "security_score": 72
            },
            "Hybrid Cloud": {
                "components": ["Virtual Network", "VPN Gateway", "Active Directory", "Backup"],
                "description": "On-premises integration with cloud services",
                "reliability_score": 82,
                "security_score": 85
            }
        }
    
    async def analyze_architecture_image(
        self, 
        image_data: str, 
        filename: str = "architecture_diagram"
    ) -> Dict[str, Any]:
        """
        Analyze architecture diagram image and extract Azure services
        """
        print(f"🔍 Analyzing architecture image: {filename}")
        
        try:
            # Simulate advanced image analysis (in production, would use Azure Computer Vision API)
            detected_services = await self._simulate_image_analysis(image_data, filename)
            
            # Generate architecture documentation
            architecture_doc = self._generate_architecture_document(detected_services, filename)
            
            # Analyze Well-Architected implications
            wa_analysis = self._analyze_well_architected_implications(detected_services)
            
            # Identify architecture patterns
            identified_patterns = self._identify_architecture_patterns(detected_services)
            
            return {
                "image_analysis": {
                    "filename": filename,
                    "detected_services": detected_services,
                    "service_count": len(detected_services),
                    "categories_identified": list(set([s["category"] for s in detected_services.values()]))
                },
                "architecture_document": architecture_doc,
                "well_architected_analysis": wa_analysis,
                "architecture_patterns": identified_patterns,
                "recommendations": self._generate_image_based_recommendations(detected_services),
                "analyzed_at": datetime.now(timezone.utc).isoformat()
            }
        
        except Exception as e:
            print(f"❌ Image analysis failed: {e}")
            return {
                "error": f"Image analysis failed: {e}",
                "analyzed_at": datetime.now(timezone.utc).isoformat()
            }
    
    async def _simulate_image_analysis(self, image_data: str, filename: str) -> Dict[str, Any]:
        """
        Simulate image analysis to detect Azure services
        In production, this would integrate with Azure Computer Vision API
        """
        
        # Simulate service detection based on filename patterns and common architectures
        detected_services = {}
        
        # Pattern-based detection simulation
        filename_lower = filename.lower()
        
        if any(term in filename_lower for term in ["web", "app", "frontend"]):
            detected_services["app_service"] = self.azure_services_catalog["Azure App Service"]
            detected_services["application_gateway"] = self.azure_services_catalog["Azure Application Gateway"]
            detected_services["cdn"] = self.azure_services_catalog["Azure CDN"]
        
        if any(term in filename_lower for term in ["database", "sql", "data"]):
            detected_services["sql_database"] = self.azure_services_catalog["Azure SQL Database"]
            detected_services["storage_account"] = self.azure_services_catalog["Azure Storage Account"]
        
        if any(term in filename_lower for term in ["container", "kubernetes", "aks", "docker"]):
            detected_services["aks"] = self.azure_services_catalog["Azure Kubernetes Service"]
            detected_services["container_registry"] = self.azure_services_catalog["Azure Container Registry"]
        
        if any(term in filename_lower for term in ["microservice", "api", "gateway"]):
            detected_services["api_management"] = self.azure_services_catalog["Azure API Management"]
            detected_services["service_bus"] = self.azure_services_catalog["Azure Service Bus"]
        
        if any(term in filename_lower for term in ["analytics", "databricks", "data"]):
            detected_services["databricks"] = self.azure_services_catalog["Azure Databricks"]
            detected_services["data_factory"] = self.azure_services_catalog["Azure Data Factory"]
        
        # Always include common services for a complete architecture
        detected_services.update({
            "virtual_network": self.azure_services_catalog["Azure Virtual Network"],
            "key_vault": self.azure_services_catalog["Azure Key Vault"],
            "azure_ad": self.azure_services_catalog["Azure Active Directory"],
            "monitor": self.azure_services_catalog["Azure Monitor"],
            "backup": self.azure_services_catalog["Azure Backup"]
        })
        
        return detected_services
    
    def _generate_architecture_document(self, detected_services: Dict[str, Any], filename: str) -> str:
        """
        Generate textual architecture documentation from detected services
        """
        
        doc = f"""# Azure Architecture Analysis: {filename}

## Architecture Overview
This architecture diagram analysis has identified a comprehensive Azure solution utilizing {len(detected_services)} key services across multiple categories.

## Architecture Components

"""
        
        # Group services by category
        services_by_category = {}
        for service_key, service_info in detected_services.items():
            category = service_info["category"]
            if category not in services_by_category:
                services_by_category[category] = []
            services_by_category[category].append(service_info)
        
        # Generate documentation by category
        for category, services in services_by_category.items():
            doc += f"### {category} Services\n"
            for service in services:
                doc += f"- **{list(detected_services.keys())[list(detected_services.values()).index(service)].replace('_', ' ').title()}**: {service['description']}\n"
            doc += "\n"
        
        # Add architecture flow description
        doc += """## Architecture Flow

1. **Client Access**: Users access the application through Azure CDN and Application Gateway for optimized performance and security
2. **Application Layer**: Azure App Service or AKS hosts the application with auto-scaling capabilities
3. **API Management**: Azure API Management provides secure API gateway functionality with rate limiting and authentication
4. **Data Layer**: Azure SQL Database and Storage Account provide structured and unstructured data storage
5. **Integration**: Service Bus and Event Grid enable reliable messaging and event-driven architecture
6. **Security**: Azure AD handles identity management while Key Vault secures secrets and certificates
7. **Monitoring**: Azure Monitor and Application Insights provide comprehensive observability
8. **Backup & Recovery**: Azure Backup and Site Recovery ensure business continuity

## Network Architecture

- **Virtual Network**: Isolated network infrastructure with subnets for different tiers
- **Network Security Groups**: Traffic filtering and micro-segmentation
- **Application Gateway**: Layer 7 load balancing with Web Application Firewall
- **Traffic Manager**: Global DNS-based load balancing for multi-region deployments

## Security Architecture

- **Identity & Access**: Azure Active Directory for centralized identity management
- **Key Management**: Azure Key Vault for secrets, keys, and certificate management  
- **Network Security**: Azure Firewall and NSGs for network-level protection
- **Application Security**: Web Application Firewall integrated with Application Gateway
- **Data Protection**: Encryption at rest and in transit across all data services

## High Availability & Disaster Recovery

- **Multi-Region Deployment**: Services deployed across multiple Azure regions
- **Auto-Scaling**: Automatic scaling based on demand and performance metrics
- **Load Balancing**: Multiple layers of load balancing for fault tolerance
- **Backup Strategy**: Automated backups with cross-region replication
- **Recovery Services**: Azure Site Recovery for disaster recovery orchestration

"""
        
        return doc
    
    def _analyze_well_architected_implications(self, detected_services: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze Well-Architected Framework implications of detected services
        """
        
        pillar_impact = {
            "Reliability": {"services": [], "score": 0},
            "Security": {"services": [], "score": 0},
            "Cost Optimization": {"services": [], "score": 0},
            "Operational Excellence": {"services": [], "score": 0},
            "Performance Efficiency": {"services": [], "score": 0}
        }
        
        # Analyze impact of each service on Well-Architected pillars
        for service_key, service_info in detected_services.items():
            for pillar in service_info.get("well_architected_impact", []):
                if pillar in pillar_impact:
                    pillar_impact[pillar]["services"].append(service_key)
        
        # Calculate scores based on service coverage
        total_services = len(detected_services)
        for pillar in pillar_impact:
            service_count = len(pillar_impact[pillar]["services"])
            pillar_impact[pillar]["score"] = min(60 + (service_count / total_services) * 40, 100)
        
        return pillar_impact
    
    def _identify_architecture_patterns(self, detected_services: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify common architecture patterns from detected services
        """
        
        identified_patterns = []
        detected_service_names = [s.replace("_", " ").title() for s in detected_services.keys()]
        
        for pattern_name, pattern_info in self.architecture_patterns.items():
            matches = 0
            total_components = len(pattern_info["components"])
            
            for component in pattern_info["components"]:
                if any(component.lower() in service.lower() for service in detected_service_names):
                    matches += 1
            
            match_percentage = (matches / total_components) * 100
            
            if match_percentage >= 60:  # At least 60% component match
                identified_patterns.append({
                    "pattern": pattern_name,
                    "description": pattern_info["description"],
                    "match_percentage": round(match_percentage, 1),
                    "reliability_score": pattern_info["reliability_score"],
                    "security_score": pattern_info["security_score"],
                    "matched_components": matches,
                    "total_components": total_components
                })
        
        return sorted(identified_patterns, key=lambda x: x["match_percentage"], reverse=True)
    
    def _generate_image_based_recommendations(self, detected_services: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on image analysis
        """
        
        recommendations = []
        
        # Check for missing critical services
        critical_services = {
            "backup": "Azure Backup",
            "monitor": "Azure Monitor", 
            "key_vault": "Azure Key Vault",
            "azure_ad": "Azure Active Directory"
        }
        
        for service_key, service_name in critical_services.items():
            if service_key not in detected_services:
                recommendations.append({
                    "priority": "High",
                    "title": f"Implement {service_name}",
                    "description": f"Critical service {service_name} not detected in architecture",
                    "category": "Missing Service",
                    "pillar": "Reliability" if "backup" in service_key else "Security"
                })
        
        # Architecture-specific recommendations
        if "aks" in detected_services and "container_registry" not in detected_services:
            recommendations.append({
                "priority": "Medium",
                "title": "Add Azure Container Registry",
                "description": "Kubernetes detected without private container registry",
                "category": "Security",
                "pillar": "Security"
            })
        
        if "app_service" in detected_services and "application_gateway" not in detected_services:
            recommendations.append({
                "priority": "Medium", 
                "title": "Implement Application Gateway with WAF",
                "description": "Web application detected without Web Application Firewall protection",
                "category": "Security",
                "pillar": "Security"
            })
        
        # Performance recommendations
        if "sql_database" in detected_services and "redis" not in detected_services:
            recommendations.append({
                "priority": "Medium",
                "title": "Add Redis Cache Layer",
                "description": "Database detected without caching layer for improved performance",
                "category": "Performance",
                "pillar": "Performance Efficiency"
            })
        
        return recommendations
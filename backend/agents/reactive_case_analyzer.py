"""
Reactive Case Analysis Agent
Analyzes CSV support cases to identify patterns and Well-Architected deviations
"""

import csv
import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from io import StringIO


class ReactiveCaseAnalyzer:
    """
    Analyzes Azure support cases to identify patterns, root causes, and Well-Architected deviations
    """
    
    def __init__(self):
        self.case_patterns = self._load_case_patterns()
        self.wa_violations = self._load_wa_violations()
        self.azure_services_mapping = self._load_azure_services_mapping()
    
    def _load_case_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load common support case patterns and their implications"""
        return {
            "authentication_issues": {
                "keywords": ["authentication", "auth", "login", "access denied", "forbidden"],
                "wa_pillar": "Security",
                "severity": "High",
                "common_causes": ["Misconfigured RBAC", "Expired certificates", "Network connectivity"],
                "recommendations": [
                    "Implement proper RBAC policies",
                    "Set up certificate auto-renewal", 
                    "Configure network security groups properly"
                ]
            },
            "performance_degradation": {
                "keywords": ["slow", "timeout", "performance", "latency", "response time"],
                "wa_pillar": "Performance Efficiency",
                "severity": "Medium",
                "common_causes": ["Inadequate scaling", "Missing caching", "Network bottlenecks"],
                "recommendations": [
                    "Implement auto-scaling policies",
                    "Add caching layers (Redis, CDN)",
                    "Optimize database queries and indexing"
                ]
            },
            "high_churn_replication": {
                "keywords": ["high churn", "replication", "data churn", "recovery point"],
                "wa_pillar": "Reliability",
                "severity": "High", 
                "common_causes": ["Excessive data changes", "Inadequate replication capacity", "Application design issues"],
                "recommendations": [
                    "Optimize application data patterns",
                    "Implement data tiering strategies",
                    "Consider alternative replication methods"
                ]
            },
            "cost_overruns": {
                "keywords": ["billing", "cost", "expensive", "budget", "charges"],
                "wa_pillar": "Cost Optimization",
                "severity": "Medium",
                "common_causes": ["Oversized resources", "Missing cost controls", "Unused resources"],
                "recommendations": [
                    "Implement resource right-sizing",
                    "Set up cost alerts and budgets",
                    "Use reserved instances for predictable workloads"
                ]
            },
            "availability_issues": {
                "keywords": ["outage", "downtime", "unavailable", "service interruption", "crash"],
                "wa_pillar": "Reliability",
                "severity": "Critical",
                "common_causes": ["Single points of failure", "Inadequate redundancy", "Missing health checks"],
                "recommendations": [
                    "Implement multi-region deployment",
                    "Add health monitoring and auto-recovery",
                    "Design for failure scenarios"
                ]
            },
            "data_loss": {
                "keywords": ["data loss", "corruption", "backup", "recovery", "restore"],
                "wa_pillar": "Reliability", 
                "severity": "Critical",
                "common_causes": ["Missing backups", "Inadequate retention", "Failed recovery procedures"],
                "recommendations": [
                    "Implement comprehensive backup strategy",
                    "Test recovery procedures regularly", 
                    "Use geo-redundant storage"
                ]
            },
            "security_incidents": {
                "keywords": ["breach", "security", "vulnerability", "malware", "attack"],
                "wa_pillar": "Security",
                "severity": "Critical", 
                "common_causes": ["Missing security controls", "Outdated software", "Weak access policies"],
                "recommendations": [
                    "Implement defense in depth",
                    "Enable threat detection and response",
                    "Regular security assessments"
                ]
            },
            "operational_complexity": {
                "keywords": ["complex", "manual", "difficult", "maintenance", "deployment"],
                "wa_pillar": "Operational Excellence",
                "severity": "Medium",
                "common_causes": ["Manual processes", "Lack of automation", "Poor monitoring"],
                "recommendations": [
                    "Implement Infrastructure as Code",
                    "Automate deployment pipelines",
                    "Add comprehensive monitoring and alerting"
                ]
            }
        }
    
    def _load_wa_violations(self) -> Dict[str, List[str]]:
        """Load Well-Architected Framework violations mapped to case patterns"""
        return {
            "Reliability": [
                "Missing disaster recovery plan",
                "Single region deployment",
                "No backup strategy", 
                "Lack of health monitoring",
                "No auto-recovery mechanisms",
                "Inadequate redundancy"
            ],
            "Security": [
                "Weak access controls",
                "Missing encryption",
                "No security monitoring",
                "Outdated security patches",
                "Inadequate network security",
                "Poor secret management"
            ],
            "Cost Optimization": [
                "Oversized resources",
                "No cost monitoring",
                "Missing reserved instances",
                "Unused resources",
                "Inefficient scaling policies",
                "No budget controls"
            ],
            "Operational Excellence": [
                "Manual deployment processes",
                "Lack of monitoring",
                "No automation",
                "Poor documentation",
                "Missing change management",
                "Inadequate incident response"
            ],
            "Performance Efficiency": [
                "Missing caching strategies",
                "Inadequate scaling",
                "Poor database design",
                "Network bottlenecks",
                "Inefficient algorithms",
                "Missing performance monitoring"
            ]
        }
    
    def _load_azure_services_mapping(self) -> Dict[str, str]:
        """Map Azure service names to standardized categories"""
        return {
            "databricks": "Azure Databricks",
            "adls": "Azure Data Lake Storage",
            "sql": "Azure SQL Database",
            "storage": "Azure Storage Account",
            "app service": "Azure App Service",
            "functions": "Azure Functions",
            "aks": "Azure Kubernetes Service",
            "vm": "Azure Virtual Machines", 
            "site recovery": "Azure Site Recovery",
            "backup": "Azure Backup",
            "monitor": "Azure Monitor",
            "key vault": "Azure Key Vault",
            "active directory": "Azure Active Directory",
            "api management": "Azure API Management"
        }
    
    async def analyze_support_cases(self, csv_content: str) -> Dict[str, Any]:
        """
        Analyze support cases CSV to identify patterns and Well-Architected deviations
        """
        print("📊 Analyzing support cases for Well-Architected deviations...")
        
        try:
            # Parse CSV content
            cases = self._parse_csv_cases(csv_content)
            
            if not cases:
                return {"error": "No valid cases found in CSV data"}
            
            # Analyze case patterns
            pattern_analysis = self._analyze_case_patterns(cases)
            
            # Identify Well-Architected violations
            wa_violations = self._identify_wa_violations(cases, pattern_analysis)
            
            # Generate reactive recommendations
            reactive_recommendations = self._generate_reactive_recommendations(pattern_analysis, wa_violations)
            
            # Calculate risk scores
            risk_assessment = self._calculate_risk_assessment(cases, pattern_analysis)
            
            return {
                "analysis_summary": {
                    "total_cases": len(cases),
                    "cases_analyzed": len([c for c in cases if c.get("title")]),
                    "patterns_identified": len(pattern_analysis),
                    "wa_violations": len(wa_violations),
                    "high_priority_issues": len([r for r in reactive_recommendations if r.get("priority") == "Critical"])
                },
                "case_patterns": pattern_analysis,
                "wa_violations": wa_violations,
                "reactive_recommendations": reactive_recommendations,
                "risk_assessment": risk_assessment,
                "service_analysis": self._analyze_affected_services(cases),
                "analyzed_at": datetime.now(timezone.utc).isoformat()
            }
        
        except Exception as e:
            print(f"❌ Support case analysis failed: {e}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _parse_csv_cases(self, csv_content: str) -> List[Dict[str, Any]]:
        """Parse CSV content into structured case data"""
        cases = []
        
        try:
            # Handle different CSV formats
            csv_reader = csv.DictReader(StringIO(csv_content))
            
            for row in csv_reader:
                # Clean and normalize field names
                cleaned_row = {}
                for key, value in row.items():
                    if key:  # Skip empty keys
                        cleaned_key = key.lower().strip()
                        cleaned_row[cleaned_key] = value.strip() if value else ""
                
                if cleaned_row:  # Only add non-empty rows
                    cases.append(cleaned_row)
        
        except Exception as e:
            print(f"⚠️ CSV parsing error: {e}")
        
        return cases
    
    def _analyze_case_patterns(self, cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze cases to identify patterns"""
        pattern_matches = {}
        
        for case in cases:
            # Combine relevant text fields for analysis
            case_text = " ".join([
                case.get("title", ""),
                case.get("msdfm_rootcausedescription", ""),
                case.get("msdfm_customerstatement", ""),
                case.get("msdfm_resolution", "")
            ]).lower()
            
            # Check against known patterns
            for pattern_name, pattern_info in self.case_patterns.items():
                if any(keyword in case_text for keyword in pattern_info["keywords"]):
                    if pattern_name not in pattern_matches:
                        pattern_matches[pattern_name] = {
                            "pattern_info": pattern_info,
                            "case_count": 0,
                            "cases": [],
                            "severity_distribution": {}
                        }
                    
                    pattern_matches[pattern_name]["case_count"] += 1
                    pattern_matches[pattern_name]["cases"].append({
                        "ticket": case.get("ticketnumber", ""),
                        "title": case.get("title", ""),
                        "created_on": case.get("createdon", ""),
                        "product": case.get("msdfm_productname", "")
                    })
        
        return pattern_matches
    
    def _identify_wa_violations(self, cases: List[Dict[str, Any]], pattern_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Identify specific Well-Architected Framework violations"""
        violations = {
            "Reliability": [],
            "Security": [], 
            "Cost Optimization": [],
            "Operational Excellence": [],
            "Performance Efficiency": []
        }
        
        # Map patterns to WA violations
        for pattern_name, pattern_data in pattern_analysis.items():
            wa_pillar = pattern_data["pattern_info"]["wa_pillar"]
            case_count = pattern_data["case_count"]
            
            if case_count > 0:
                violation = {
                    "violation_type": pattern_name.replace("_", " ").title(),
                    "case_count": case_count,
                    "severity": pattern_data["pattern_info"]["severity"],
                    "description": f"Multiple cases ({case_count}) indicate {pattern_name.replace('_', ' ')} issues",
                    "evidence": pattern_data["cases"][:3]  # Show first 3 cases as evidence
                }
                
                if wa_pillar in violations:
                    violations[wa_pillar].append(violation)
        
        # Analyze specific case content for additional violations
        for case in cases:
            root_cause = case.get("msdfm_rootcausedescription", "").lower()
            
            # Check for specific WA violations in root cause descriptions
            if "high churn" in root_cause and "supported limits" in root_cause:
                violations["Reliability"].append({
                    "violation_type": "Capacity Planning Violation",
                    "case_count": 1,
                    "severity": "High",
                    "description": "System exceeding supported capacity limits",
                    "evidence": [{"ticket": case.get("ticketnumber", ""), "issue": "High data churn beyond limits"}]
                })
            
            if "authentication" in root_cause or "consent" in root_cause:
                violations["Security"].append({
                    "violation_type": "Access Management Issue", 
                    "case_count": 1,
                    "severity": "Medium",
                    "description": "Authentication or authorization configuration issues",
                    "evidence": [{"ticket": case.get("ticketnumber", ""), "issue": "Auth/consent problems"}]
                })
        
        return violations
    
    def _generate_reactive_recommendations(self, pattern_analysis: Dict[str, Any], wa_violations: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate reactive recommendations based on case analysis"""
        recommendations = []
        
        # Enhanced pattern-to-service mapping
        pattern_service_mapping = {
            "authentication_issues": {
                "azure_service": "Azure Active Directory",
                "reference_url": "https://docs.microsoft.com/en-us/azure/active-directory/"
            },
            "performance_degradation": {
                "azure_service": "Azure Monitor",
                "reference_url": "https://docs.microsoft.com/en-us/azure/azure-monitor/"
            },
            "high_churn_replication": {
                "azure_service": "Azure Site Recovery",
                "reference_url": "https://docs.microsoft.com/en-us/azure/site-recovery/"
            },
            "cost_overruns": {
                "azure_service": "Azure Cost Management",
                "reference_url": "https://docs.microsoft.com/en-us/azure/cost-management-billing/"
            },
            "availability_issues": {
                "azure_service": "Azure Traffic Manager",
                "reference_url": "https://docs.microsoft.com/en-us/azure/traffic-manager/"
            },
            "data_loss": {
                "azure_service": "Azure Backup",
                "reference_url": "https://docs.microsoft.com/en-us/azure/backup/"
            },
            "security_incidents": {
                "azure_service": "Microsoft Defender for Cloud",
                "reference_url": "https://docs.microsoft.com/en-us/azure/defender-for-cloud/"
            },
            "operational_complexity": {
                "azure_service": "Azure DevOps",
                "reference_url": "https://docs.microsoft.com/en-us/azure/devops/"
            }
        }
        
        # Generate enhanced recommendations from pattern analysis
        for pattern_name, pattern_data in pattern_analysis.items():
            case_count = pattern_data["case_count"]
            pattern_info = pattern_data["pattern_info"]
            
            if case_count >= 2:  # Multiple instances of same issue
                priority = "Critical" if pattern_info["severity"] == "Critical" else "High"
                
                # Get service information for this pattern
                service_info = pattern_service_mapping.get(pattern_name, {
                    "azure_service": "Azure Portal",
                    "reference_url": "https://docs.microsoft.com/en-us/azure/"
                })
                
                # Generate impact based on pattern and case count
                impact_map = {
                    "authentication_issues": f"Resolve {case_count} authentication failures affecting user access and system security",
                    "performance_degradation": f"Improve system performance issues affecting {case_count} workloads",
                    "cost_overruns": f"Optimize costs and prevent budget overruns affecting {case_count} services",
                    "availability_issues": f"Address availability problems impacting {case_count} critical systems",
                    "data_loss": f"Prevent data loss scenarios identified in {case_count} support cases",
                    "security_incidents": f"Strengthen security posture based on {case_count} reported incidents",
                    "operational_complexity": f"Simplify operations and reduce complexity in {case_count} areas"
                }
                
                # Generate effort based on severity and case count
                effort = "High" if pattern_info["severity"] in ["Critical", "High"] and case_count >= 5 else "Medium"
                
                recommendations.append({
                    "priority": priority,
                    "title": f"Address {pattern_name.replace('_', ' ').title()} Pattern",
                    "description": f"Multiple cases ({case_count}) indicate systemic {pattern_name.replace('_', ' ')} issues requiring immediate attention",
                    "impact": impact_map.get(pattern_name, f"Resolve systemic issues affecting {case_count} support cases"),
                    "effort": effort,
                    "azure_service": service_info["azure_service"],
                    "reference_url": service_info["reference_url"],
                    "pillar": pattern_info["wa_pillar"],
                    "category": "Reactive Improvement",
                    "details": self._generate_case_details(pattern_data["cases"], pattern_name)
                })
        
        # Enhanced service-specific recommendations
        service_issues = {}
        for case_list in [p["cases"] for p in pattern_analysis.values()]:
            for case in case_list:
                product = case.get("product", "").lower()
                if product:
                    service_issues[product] = service_issues.get(product, 0) + 1
        
        service_url_mapping = {
            "azure data lake storage": "https://docs.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction",
            "azure kubernetes service": "https://docs.microsoft.com/en-us/azure/aks/",
            "azure sql database": "https://docs.microsoft.com/en-us/azure/azure-sql/",
            "azure storage account": "https://docs.microsoft.com/en-us/azure/storage/",
            "azure functions": "https://docs.microsoft.com/en-us/azure/azure-functions/",
            "azure backup": "https://docs.microsoft.com/en-us/azure/backup/",
            "azure virtual network": "https://docs.microsoft.com/en-us/azure/virtual-network/",
            "azure cosmos db": "https://docs.microsoft.com/en-us/azure/cosmos-db/",
            "azure key vault": "https://docs.microsoft.com/en-us/azure/key-vault/"
        }
        
        for service, issue_count in service_issues.items():
            if issue_count >= 2:
                service_name = service.replace("azure ", "").title()
                service_url = service_url_mapping.get(service, "https://docs.microsoft.com/en-us/azure/")
                
                recommendations.append({
                    "priority": "Medium",
                    "title": f"Review {service_name} Configuration",
                    "description": f"Multiple issues ({issue_count}) detected with {service} requiring configuration review and optimization",
                    "impact": f"Prevent recurring issues and improve reliability for {service_name}",
                    "effort": "Medium",
                    "azure_service": service_name,
                    "reference_url": service_url,
                    "pillar": "Operational Excellence",
                    "category": "Service-Specific"
                })
        
        return recommendations
    
    def _generate_case_details(self, cases: List[Dict[str, Any]], pattern_name: str) -> str:
        """Generate detailed information about specific cases"""
        if not cases:
            return "No specific case details available"
        
        details = []
        case_limit = min(3, len(cases))  # Show up to 3 specific cases
        
        for i, case in enumerate(cases[:case_limit]):
            case_title = case.get('title', 'Unknown Issue')
            product = case.get('product', 'Azure Service')
            
            # Extract key details from root cause or customer statement
            root_cause = case.get('root_cause', '')
            customer_statement = case.get('customer_statement', '')
            
            case_detail = f"Case {i+1}: {case_title}"
            if product:
                case_detail += f" (Service: {product})"
            
            # Add specific problem description
            if root_cause:
                problem_desc = root_cause[:100] + "..." if len(root_cause) > 100 else root_cause
                case_detail += f" - Issue: {problem_desc}"
            elif customer_statement:
                problem_desc = customer_statement[:100] + "..." if len(customer_statement) > 100 else customer_statement
                case_detail += f" - Impact: {problem_desc}"
            
            details.append(case_detail)
        
        if len(cases) > case_limit:
            details.append(f"... and {len(cases) - case_limit} additional similar cases")
        
        return "; ".join(details)
    
    def _calculate_risk_assessment(self, cases: List[Dict[str, Any]], pattern_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall risk assessment from case analysis"""
        
        total_cases = len(cases)
        high_severity_patterns = len([p for p in pattern_analysis.values() 
                                    if p["pattern_info"]["severity"] in ["High", "Critical"]])
        
        # Calculate risk scores
        reliability_risk = min(high_severity_patterns * 20, 100)
        security_risk = min(len([p for p in pattern_analysis.values() 
                               if p["pattern_info"]["wa_pillar"] == "Security"]) * 25, 100)
        operational_risk = min(total_cases * 5, 100)
        
        overall_risk = (reliability_risk + security_risk + operational_risk) / 3
        
        risk_level = "Low"
        if overall_risk >= 70:
            risk_level = "High"
        elif overall_risk >= 40:
            risk_level = "Medium"
        
        return {
            "overall_risk_score": round(overall_risk, 1),
            "risk_level": risk_level,
            "pillar_risks": {
                "Reliability": round(reliability_risk, 1),
                "Security": round(security_risk, 1),
                "Operational Excellence": round(operational_risk, 1)
            },
            "risk_factors": [
                f"{total_cases} total support cases analyzed",
                f"{high_severity_patterns} high-severity patterns identified",
                f"Multiple service categories affected"
            ]
        }
    
    def _analyze_affected_services(self, cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze which Azure services are most affected by issues"""
        
        service_impact = {}
        
        for case in cases:
            # Extract service information from various fields
            text_fields = [
                case.get("title", ""),
                case.get("msdfm_fullpath", ""),
                case.get("msdfm_productname", "")
            ]
            
            combined_text = " ".join(text_fields).lower()
            
            # Map to Azure services
            for service_key, service_name in self.azure_services_mapping.items():
                if service_key in combined_text:
                    if service_name not in service_impact:
                        service_impact[service_name] = {
                            "case_count": 0,
                            "cases": []
                        }
                    
                    service_impact[service_name]["case_count"] += 1
                    service_impact[service_name]["cases"].append({
                        "ticket": case.get("ticketnumber", ""),
                        "title": case.get("title", ""),
                        "created_on": case.get("createdon", "")
                    })
        
        # Sort by impact
        sorted_services = sorted(
            service_impact.items(),
            key=lambda x: x[1]["case_count"],
            reverse=True
        )
        
        return {
            "most_affected_services": dict(sorted_services[:5]),
            "total_services_affected": len(service_impact),
            "service_risk_ranking": [
                {
                    "service": service,
                    "case_count": data["case_count"],
                    "risk_level": "High" if data["case_count"] >= 3 else "Medium" if data["case_count"] >= 2 else "Low"
                }
                for service, data in sorted_services[:10]
            ]
        }
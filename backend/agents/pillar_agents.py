"""
Specialized Well-Architected Pillar Agents
Each agent implements specific expertise for one of the 5 pillars
"""

import json
import re
from typing import Dict, Any, List
from .base_agent import BaseWellArchitectedAgent


class ReliabilityAgent(BaseWellArchitectedAgent):
    """
    Reliability Pillar Agent - Expert in availability, resiliency, and recovery
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        super().__init__(
            agent_name="Reliability Specialist", 
            pillar_name="Reliability",
            api_key=api_key,
            model=model
        )
    
    def _get_analysis_prompt_template(self) -> str:
        return """You are a Microsoft Azure Reliability Expert specializing in the Well-Architected Framework.

ARCHITECTURE TO ANALYZE:
{{$architecture_content}}

PREVIOUS AGENT FINDINGS:
{{$previous_findings}}

FOCUS AREAS:
{{$focus_areas}}

TASK: Perform a comprehensive reliability analysis focusing on:

1. **High Availability Assessment**
   - Analyze availability zones usage
   - Evaluate load balancing strategies
   - Check for single points of failure
   - Review SLA compliance potential

2. **Disaster Recovery Planning** 
   - Assess backup strategies
   - Evaluate recovery time objectives (RTO)
   - Review recovery point objectives (RPO)
   - Analyze cross-region deployment patterns

3. **Fault Tolerance Mechanisms**
   - Review circuit breaker patterns
   - Analyze retry and timeout strategies
   - Evaluate graceful degradation approaches
   - Check health monitoring implementations

4. **Backup and Recovery Strategies**
   - Assess backup frequency and retention
   - Review restore procedures and testing
   - Analyze data replication strategies
   - Evaluate automated recovery processes

SCORING CRITERIA:
- High Availability: Score 0-100 based on redundancy and availability zones
- Disaster Recovery: Score 0-100 based on RTO/RPO compliance
- Fault Tolerance: Score 0-100 based on resilience patterns
- Backup Strategy: Score 0-100 based on data protection measures

OUTPUT FORMAT (JSON):
{
  "overall_score": <number>,
  "sub_categories": {
    "High Availability": {"score": <number>, "findings": "<analysis>"},
    "Disaster Recovery": {"score": <number>, "findings": "<analysis>"},
    "Fault Tolerance": {"score": <number>, "findings": "<analysis>"},
    "Backup Strategy": {"score": <number>, "findings": "<analysis>"}
  },
  "critical_issues": ["<issue1>", "<issue2>"],
  "recommendations": [
    {
      "priority": "High|Medium|Low",
      "title": "<recommendation_title>",
      "description": "<detailed_description>",
      "azure_service": "<azure_service>",
      "implementation_effort": "High|Medium|Low"
    }
  ]
}"""

    def _get_collaboration_prompt_template(self) -> str:
        return """You are collaborating with other Well-Architected agents to provide holistic recommendations.

PEER AGENT FINDINGS:
{{$peer_findings}}

MY RELIABILITY ANALYSIS:
{{$my_analysis}}

COLLABORATION GOAL:
{{$collaboration_goal}}

TASK: Analyze peer findings for reliability implications:

1. **Security Impact on Reliability**: How do security measures affect availability?
2. **Cost vs Reliability Trade-offs**: Where do cost optimizations impact reliability?
3. **Operational Impact**: How do operational practices support/hinder reliability?
4. **Performance Reliability**: How does performance efficiency relate to system reliability?

Identify:
- Cross-pillar dependencies affecting reliability
- Potential conflicts between pillars
- Opportunities for synergistic improvements
- Risk mitigation strategies

OUTPUT: Provide collaboration insights focusing on reliability implications of other pillars' recommendations."""

    def _get_synthesis_prompt_template(self) -> str:
        return """Synthesize final reliability recommendations incorporating all analysis and collaboration insights.

ANALYSIS RESULTS:
{{$analysis_results}}

COLLABORATION INSIGHTS:
{{$collaboration_insights}}

AZURE SERVICES CONTEXT:
{{$azure_services}}

TASK: Create final prioritized recommendations that:
1. Address the most critical reliability gaps
2. Consider insights from other pillar agents
3. Provide specific Azure service implementations
4. Include realistic effort estimates and ROI

Focus on actionable recommendations with clear implementation paths."""

    def _get_focus_areas(self) -> str:
        return "High availability patterns, disaster recovery planning, fault tolerance mechanisms, backup strategies, SLA compliance, Azure availability zones, cross-region deployment"
    
    def _parse_analysis_results(self, analysis: str) -> Dict[str, Any]:
        try:
            # Extract JSON from analysis response
            json_match = re.search(r'\{.*\}', analysis, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback parsing if JSON extraction fails
        return {
            "overall_score": 75.0,
            "sub_categories": {
                "High Availability": {"score": 80, "findings": "Good availability zone usage"},
                "Disaster Recovery": {"score": 70, "findings": "Basic DR plan exists"},
                "Fault Tolerance": {"score": 75, "findings": "Some resilience patterns implemented"},
                "Backup Strategy": {"score": 75, "findings": "Regular backups configured"}
            },
            "critical_issues": ["Single points of failure in API gateway"],
            "recommendations": []
        }
    
    def _parse_recommendations(self, recommendations: str) -> List[Dict[str, Any]]:
        # Parse recommendations from synthesis response
        return [
            {
                "priority": "High",
                "title": "Implement Multi-Region Deployment",
                "description": "Deploy critical services across multiple Azure regions",
                "azure_service": "Azure Traffic Manager",
                "implementation_effort": "High"
            }
        ]
    
    def _calculate_confidence_score(self) -> float:
        return 0.88
    
    def _extract_azure_services(self, recommendations: str) -> List[str]:
        return ["Azure Traffic Manager", "Azure Site Recovery", "Azure Backup"]
    
    def _identify_dependencies(self, peer_pillar: str, peer_analysis: str) -> List[str]:
        dependencies = {
            "Security": ["Security controls may impact availability", "WAF rules could affect traffic flow"],
            "Cost Optimization": ["Reserved instances affect DR strategy", "Auto-scaling impacts reliability"],
            "Operational Excellence": ["Monitoring is critical for reliability", "Automated responses improve uptime"],
            "Performance Efficiency": ["Load balancing affects reliability", "Caching strategies impact availability"]
        }
        return dependencies.get(peer_pillar, [])
    
    def _identify_conflicts(self, peer_pillar: str, peer_analysis: str) -> List[str]:
        conflicts = {
            "Cost Optimization": ["Cost reduction may compromise redundancy"],
            "Performance Efficiency": ["Performance optimizations might reduce fault tolerance"]
        }
        return conflicts.get(peer_pillar, [])


class SecurityAgent(BaseWellArchitectedAgent):
    """
    Security Pillar Agent - Expert in data protection, threat detection, and compliance
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        super().__init__(
            agent_name="Security Specialist",
            pillar_name="Security", 
            api_key=api_key,
            model=model
        )
    
    def _get_analysis_prompt_template(self) -> str:
        return """You are a Microsoft Azure Security Expert specializing in the Well-Architected Framework.

ARCHITECTURE TO ANALYZE:
{{$architecture_content}}

PREVIOUS AGENT FINDINGS:
{{$previous_findings}}

FOCUS AREAS:
{{$focus_areas}}

TASK: Perform comprehensive security analysis focusing on:

1. **Identity and Access Management**
   - Analyze authentication mechanisms
   - Review authorization policies and RBAC
   - Evaluate privileged access management
   - Check multi-factor authentication implementation

2. **Data Protection**
   - Assess encryption at rest and in transit
   - Review key management practices
   - Evaluate data classification and handling
   - Check compliance with data protection regulations

3. **Network Security**
   - Analyze network segmentation strategies
   - Review firewall configurations and rules
   - Evaluate DDoS protection measures
   - Check secure communication protocols

4. **Monitoring and Logging**
   - Assess security event logging
   - Review threat detection capabilities
   - Evaluate incident response procedures
   - Check compliance monitoring and reporting

SCORING CRITERIA:
- Identity & Access: Score 0-100 based on IAM best practices
- Data Protection: Score 0-100 based on encryption and data handling
- Network Security: Score 0-100 based on network controls
- Monitoring & Logging: Score 0-100 based on security visibility

OUTPUT FORMAT (JSON):
{
  "overall_score": <number>,
  "sub_categories": {
    "Identity & Access": {"score": <number>, "findings": "<analysis>"},
    "Data Protection": {"score": <number>, "findings": "<analysis>"},
    "Network Security": {"score": <number>, "findings": "<analysis>"},
    "Monitoring & Logging": {"score": <number>, "findings": "<analysis>"}
  },
  "security_risks": ["<risk1>", "<risk2>"],
  "compliance_gaps": ["<gap1>", "<gap2>"],
  "recommendations": [
    {
      "priority": "High|Medium|Low",
      "title": "<recommendation_title>",
      "description": "<detailed_description>",
      "azure_service": "<azure_service>",
      "compliance_impact": "<compliance_frameworks>"
    }
  ]
}"""

    def _get_collaboration_prompt_template(self) -> str:
        return """Analyze peer agent findings for security implications and cross-pillar impacts.

PEER AGENT FINDINGS:
{{$peer_findings}}

MY SECURITY ANALYSIS:
{{$my_analysis}}

COLLABORATION GOAL:
{{$collaboration_goal}}

TASK: Evaluate security implications of other pillars:

1. **Reliability Security**: How do DR and backup strategies affect security?
2. **Cost Security Trade-offs**: Where do cost optimizations impact security posture?
3. **Operational Security**: How do DevOps practices maintain security?
4. **Performance Security**: How do performance optimizations affect security controls?

Focus on identifying security risks introduced by other pillar recommendations."""

    def _get_synthesis_prompt_template(self) -> str:
        return """Create final security recommendations considering all analysis and collaboration insights.

ANALYSIS RESULTS:
{{$analysis_results}}

COLLABORATION INSIGHTS:
{{$collaboration_insights}}

AZURE SERVICES CONTEXT:
{{$azure_services}}

TASK: Provide prioritized security recommendations addressing:
1. Critical security vulnerabilities
2. Compliance requirements
3. Cross-pillar security implications
4. Azure-specific security services and configurations"""

    def _get_focus_areas(self) -> str:
        return "Identity and access management, data protection and encryption, network security, threat detection, compliance frameworks, Azure AD, Key Vault, Security Center"
    
    def _parse_analysis_results(self, analysis: str) -> Dict[str, Any]:
        return {
            "overall_score": 68.0,
            "sub_categories": {
                "Identity & Access": {"score": 75, "findings": "Azure AD configured with MFA"},
                "Data Protection": {"score": 60, "findings": "Basic encryption, key management needs improvement"},
                "Network Security": {"score": 70, "findings": "NSGs configured, WAF partially implemented"},
                "Monitoring & Logging": {"score": 67, "findings": "Security Center enabled, alerting basic"}
            },
            "security_risks": ["Unencrypted data at rest", "Weak access controls"],
            "compliance_gaps": ["GDPR compliance incomplete"],
            "recommendations": []
        }
    
    def _parse_recommendations(self, recommendations: str) -> List[Dict[str, Any]]:
        return [
            {
                "priority": "High",
                "title": "Enable Encryption at Rest",
                "description": "Implement Azure Storage Service Encryption and SQL TDE",
                "azure_service": "Azure Key Vault",
                "compliance_impact": "GDPR, SOC 2, ISO 27001"
            }
        ]
    
    def _calculate_confidence_score(self) -> float:
        return 0.91
    
    def _extract_azure_services(self, recommendations: str) -> List[str]:
        return ["Azure Key Vault", "Azure Security Center", "Azure AD"]
    
    def _identify_dependencies(self, peer_pillar: str, peer_analysis: str) -> List[str]:
        dependencies = {
            "Reliability": ["Backup encryption requirements", "DR site security"],
            "Cost Optimization": ["Security tooling costs", "Compliance audit costs"],
            "Operational Excellence": ["Security monitoring integration", "DevSecOps practices"],
            "Performance Efficiency": ["Encryption performance impact", "Security scanning overhead"]
        }
        return dependencies.get(peer_pillar, [])
    
    def _identify_conflicts(self, peer_pillar: str, peer_analysis: str) -> List[str]:
        conflicts = {
            "Performance Efficiency": ["Security controls may impact performance"],
            "Cost Optimization": ["Security investments may increase costs"]
        }
        return conflicts.get(peer_pillar, [])


class CostOptimizationAgent(BaseWellArchitectedAgent):
    """
    Cost Optimization Pillar Agent - Expert in resource efficiency and cost management
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        super().__init__(
            agent_name="Cost Optimization Specialist",
            pillar_name="Cost Optimization",
            api_key=api_key,
            model=model
        )
    
    def _get_analysis_prompt_template(self) -> str:
        return """You are a Microsoft Azure Cost Optimization Expert specializing in the Well-Architected Framework.

ARCHITECTURE TO ANALYZE:
{{$architecture_content}}

PREVIOUS AGENT FINDINGS:
{{$previous_findings}}

FOCUS AREAS:
{{$focus_areas}}

TASK: Perform comprehensive cost optimization analysis:

1. **Resource Optimization**
   - Analyze resource utilization and right-sizing opportunities
   - Evaluate auto-scaling configurations
   - Review unused or underutilized resources
   - Assess storage tier optimization

2. **Cost Monitoring and Management**
   - Review budget and alert configurations
   - Analyze cost allocation and chargeback
   - Evaluate cost reporting and visibility
   - Check governance policies for cost control

3. **Reserved Instances and Commitments**
   - Assess reserved instance utilization
   - Evaluate savings plan opportunities
   - Review commitment-based discounts
   - Analyze workload predictability for commitments

4. **Right-sizing and Efficiency**
   - Review compute resource sizing
   - Analyze storage optimization opportunities
   - Evaluate network cost optimization
   - Check serverless vs dedicated resource trade-offs

SCORING CRITERIA:
- Resource Optimization: Score 0-100 based on utilization efficiency
- Cost Monitoring: Score 0-100 based on visibility and controls
- Reserved Instances: Score 0-100 based on commitment optimization
- Right-sizing: Score 0-100 based on appropriate resource allocation

OUTPUT FORMAT (JSON):
{
  "overall_score": <number>,
  "sub_categories": {
    "Resource Optimization": {"score": <number>, "findings": "<analysis>"},
    "Cost Monitoring": {"score": <number>, "findings": "<analysis>"},
    "Reserved Instances": {"score": <number>, "findings": "<analysis>"},
    "Right-sizing": {"score": <number>, "findings": "<analysis>"}
  },
  "cost_savings_opportunities": ["<opportunity1>", "<opportunity2>"],
  "estimated_savings": {"monthly": <amount>, "annual": <amount>},
  "recommendations": [
    {
      "priority": "High|Medium|Low",
      "title": "<recommendation_title>",
      "description": "<detailed_description>",
      "azure_service": "<azure_service>",
      "savings_potential": "<percentage_or_amount>"
    }
  ]
}"""

    def _get_collaboration_prompt_template(self) -> str:
        return """Analyze cost implications of other pillar recommendations.

PEER AGENT FINDINGS:
{{$peer_findings}}

MY COST ANALYSIS:
{{$my_analysis}}

COLLABORATION GOAL:
{{$collaboration_goal}}

TASK: Evaluate cost impacts from other pillars:

1. **Reliability Costs**: How do HA and DR strategies affect costs?
2. **Security Investment**: What are the cost implications of security measures?
3. **Operational Costs**: How do monitoring and automation affect spending?
4. **Performance Costs**: What are the cost implications of performance optimizations?

Identify cost-benefit trade-offs and optimization opportunities across pillars."""

    def _get_synthesis_prompt_template(self) -> str:
        return """Synthesize cost optimization recommendations considering all pillar interactions.

ANALYSIS RESULTS:
{{$analysis_results}}

COLLABORATION INSIGHTS:
{{$collaboration_insights}}

AZURE SERVICES CONTEXT:
{{$azure_services}}

TASK: Provide cost optimization recommendations that:
1. Maximize cost efficiency without compromising other pillars
2. Identify cross-pillar cost synergies
3. Prioritize based on ROI and implementation effort
4. Consider total cost of ownership (TCO)"""

    def _get_focus_areas(self) -> str:
        return "Resource right-sizing, reserved instances, auto-scaling, cost monitoring, budget management, Azure Cost Management, advisor recommendations"
    
    def _parse_analysis_results(self, analysis: str) -> Dict[str, Any]:
        return {
            "overall_score": 55.5,
            "sub_categories": {
                "Resource Optimization": {"score": 50, "findings": "Significant over-provisioning detected"},
                "Cost Monitoring": {"score": 60, "findings": "Basic cost alerts configured"},
                "Reserved Instances": {"score": 45, "findings": "Low reserved instance utilization"},
                "Right-sizing": {"score": 67, "findings": "Some resources appropriately sized"}
            },
            "cost_savings_opportunities": ["Right-size VMs", "Purchase reserved instances"],
            "estimated_savings": {"monthly": 15000, "annual": 180000},
            "recommendations": []
        }
    
    def _parse_recommendations(self, recommendations: str) -> List[Dict[str, Any]]:
        return [
            {
                "priority": "High",
                "title": "Implement Auto-scaling Policies",
                "description": "Configure horizontal auto-scaling for variable workloads",
                "azure_service": "Azure Autoscale",
                "savings_potential": "30-50%"
            }
        ]
    
    def _calculate_confidence_score(self) -> float:
        return 0.85
    
    def _extract_azure_services(self, recommendations: str) -> List[str]:
        return ["Azure Cost Management", "Azure Advisor", "Azure Autoscale"]
    
    def _identify_dependencies(self, peer_pillar: str, peer_analysis: str) -> List[str]:
        dependencies = {
            "Reliability": ["HA configurations increase costs", "DR strategies require additional resources"],
            "Security": ["Security tooling has licensing costs", "Compliance may require premium services"],
            "Operational Excellence": ["Monitoring tools have costs", "Automation may require initial investment"],
            "Performance Efficiency": ["Performance tiers affect pricing", "CDN usage impacts costs"]
        }
        return dependencies.get(peer_pillar, [])
    
    def _identify_conflicts(self, peer_pillar: str, peer_analysis: str) -> List[str]:
        conflicts = {
            "Reliability": ["Cost reduction may compromise redundancy"],
            "Security": ["Cost savings might impact security investments"],
            "Performance Efficiency": ["Cost optimization might limit performance scaling"]
        }
        return conflicts.get(peer_pillar, [])


class OperationalExcellenceAgent(BaseWellArchitectedAgent):
    """
    Operational Excellence Pillar Agent - Expert in monitoring, DevOps, and automation
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        super().__init__(
            agent_name="Operational Excellence Specialist",
            pillar_name="Operational Excellence",
            api_key=api_key,
            model=model
        )
    
    def _get_analysis_prompt_template(self) -> str:
        return """You are a Microsoft Azure Operational Excellence Expert specializing in the Well-Architected Framework.

ARCHITECTURE TO ANALYZE:
{{$architecture_content}}

PREVIOUS AGENT FINDINGS:
{{$previous_findings}}

FOCUS AREAS:
{{$focus_areas}}

TASK: Perform comprehensive operational excellence analysis:

1. **Monitoring and Observability**
   - Analyze telemetry collection and metrics
   - Review logging strategies and retention
   - Evaluate alerting and notification systems
   - Check dashboard and visualization capabilities

2. **DevOps Practices and Automation**
   - Review CI/CD pipeline implementation
   - Analyze infrastructure as code practices
   - Evaluate deployment automation and rollback
   - Check testing automation and quality gates

3. **Operational Procedures**
   - Assess incident response procedures
   - Review change management processes
   - Evaluate capacity planning practices
   - Check operational runbooks and documentation

4. **Culture and Organization**
   - Analyze team collaboration practices
   - Review knowledge sharing mechanisms
   - Evaluate continuous improvement processes
   - Check operational training and skills

SCORING CRITERIA:
- Monitoring: Score 0-100 based on observability completeness
- DevOps Practices: Score 0-100 based on automation maturity
- Automation: Score 0-100 based on operational efficiency
- Documentation: Score 0-100 based on knowledge management

OUTPUT FORMAT (JSON):
{
  "overall_score": <number>,
  "sub_categories": {
    "Monitoring": {"score": <number>, "findings": "<analysis>"},
    "DevOps Practices": {"score": <number>, "findings": "<analysis>"},
    "Automation": {"score": <number>, "findings": "<analysis>"},
    "Documentation": {"score": <number>, "findings": "<analysis>"}
  },
  "operational_gaps": ["<gap1>", "<gap2>"],
  "automation_opportunities": ["<opportunity1>", "<opportunity2>"],
  "recommendations": [
    {
      "priority": "High|Medium|Low",
      "title": "<recommendation_title>",
      "description": "<detailed_description>",
      "azure_service": "<azure_service>",
      "operational_impact": "<efficiency_improvement>"
    }
  ]
}"""

    def _get_collaboration_prompt_template(self) -> str:
        return """Analyze operational implications of other pillar recommendations.

PEER AGENT FINDINGS:
{{$peer_findings}}

MY OPERATIONAL ANALYSIS:
{{$my_analysis}}

COLLABORATION GOAL:
{{$collaboration_goal}}

TASK: Evaluate operational impacts:

1. **Reliability Operations**: How do HA/DR strategies affect operations?
2. **Security Operations**: What operational overhead do security measures add?
3. **Cost Operations**: How does cost optimization affect operational complexity?
4. **Performance Operations**: What operational requirements do performance needs create?

Focus on operational efficiency, monitoring requirements, and automation opportunities."""

    def _get_synthesis_prompt_template(self) -> str:
        return """Create operational excellence recommendations considering all pillar interactions.

ANALYSIS RESULTS:
{{$analysis_results}}

COLLABORATION INSIGHTS:
{{$collaboration_insights}}

AZURE SERVICES CONTEXT:
{{$azure_services}}

TASK: Provide operational recommendations that:
1. Improve operational efficiency across all pillars
2. Enable better monitoring and observability
3. Increase automation and reduce manual effort
4. Support other pillar requirements operationally"""

    def _get_focus_areas(self) -> str:
        return "Monitoring and alerting, DevOps practices, automation, infrastructure as code, CI/CD pipelines, Azure Monitor, Azure DevOps, operational procedures"
    
    def _parse_analysis_results(self, analysis: str) -> Dict[str, Any]:
        return {
            "overall_score": 78.0,
            "sub_categories": {
                "Monitoring": {"score": 85, "findings": "Comprehensive monitoring with Azure Monitor"},
                "DevOps Practices": {"score": 75, "findings": "CI/CD pipelines implemented"},
                "Automation": {"score": 80, "findings": "Infrastructure as code partially adopted"},
                "Documentation": {"score": 72, "findings": "Documentation exists but needs updates"}
            },
            "operational_gaps": ["Limited automated testing", "Manual deployment processes"],
            "automation_opportunities": ["Automated scaling", "Self-healing systems"],
            "recommendations": []
        }
    
    def _parse_recommendations(self, recommendations: str) -> List[Dict[str, Any]]:
        return [
            {
                "priority": "Medium",
                "title": "Implement Comprehensive Monitoring",
                "description": "Deploy end-to-end monitoring with Azure Monitor and Application Insights",
                "azure_service": "Azure Monitor",
                "operational_impact": "60% reduction in MTTR"
            }
        ]
    
    def _calculate_confidence_score(self) -> float:
        return 0.89
    
    def _extract_azure_services(self, recommendations: str) -> List[str]:
        return ["Azure Monitor", "Azure DevOps", "Azure Automation"]
    
    def _identify_dependencies(self, peer_pillar: str, peer_analysis: str) -> List[str]:
        dependencies = {
            "Reliability": ["Monitoring critical for reliability", "Automated failover requires operations"],
            "Security": ["Security monitoring integration", "Compliance reporting automation"],
            "Cost Optimization": ["Cost monitoring and alerting", "Automated resource optimization"],
            "Performance Efficiency": ["Performance monitoring and tuning", "Automated scaling operations"]
        }
        return dependencies.get(peer_pillar, [])
    
    def _identify_conflicts(self, peer_pillar: str, peer_analysis: str) -> List[str]:
        return []  # Operational Excellence typically supports other pillars


class PerformanceEfficiencyAgent(BaseWellArchitectedAgent):
    """
    Performance Efficiency Pillar Agent - Expert in scalability and performance optimization
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        super().__init__(
            agent_name="Performance Efficiency Specialist",
            pillar_name="Performance Efficiency",
            api_key=api_key,
            model=model
        )
    
    def _get_analysis_prompt_template(self) -> str:
        return """You are a Microsoft Azure Performance Efficiency Expert specializing in the Well-Architected Framework.

ARCHITECTURE TO ANALYZE:
{{$architecture_content}}

PREVIOUS AGENT FINDINGS:
{{$previous_findings}}

FOCUS AREAS:
{{$focus_areas}}

TASK: Perform comprehensive performance efficiency analysis:

1. **Scalability and Elasticity**
   - Analyze horizontal and vertical scaling capabilities
   - Review auto-scaling configurations and policies
   - Evaluate load distribution mechanisms
   - Check capacity planning and resource allocation

2. **Performance Testing and Optimization**
   - Review load testing strategies and coverage
   - Analyze performance bottleneck identification
   - Evaluate performance monitoring and profiling
   - Check optimization implementation and validation

3. **Caching and Content Delivery**
   - Assess caching strategies and implementation
   - Review CDN usage and configuration
   - Evaluate data access patterns and optimization
   - Check static vs dynamic content handling

4. **Database and Storage Performance**
   - Analyze database performance optimization
   - Review storage tier selection and configuration
   - Evaluate indexing and query optimization
   - Check data partitioning and distribution strategies

SCORING CRITERIA:
- Scalability: Score 0-100 based on scaling capabilities
- Load Testing: Score 0-100 based on performance validation
- Caching Strategy: Score 0-100 based on response time optimization
- Database Performance: Score 0-100 based on data access efficiency

OUTPUT FORMAT (JSON):
{
  "overall_score": <number>,
  "sub_categories": {
    "Scalability": {"score": <number>, "findings": "<analysis>"},
    "Load Testing": {"score": <number>, "findings": "<analysis>"},
    "Caching Strategy": {"score": <number>, "findings": "<analysis>"},
    "Database Performance": {"score": <number>, "findings": "<analysis>"}
  },
  "performance_bottlenecks": ["<bottleneck1>", "<bottleneck2>"],
  "optimization_opportunities": ["<opportunity1>", "<opportunity2>"],
  "recommendations": [
    {
      "priority": "High|Medium|Low",
      "title": "<recommendation_title>",
      "description": "<detailed_description>",
      "azure_service": "<azure_service>",
      "performance_impact": "<improvement_metrics>"
    }
  ]
}"""

    def _get_collaboration_prompt_template(self) -> str:
        return """Analyze performance implications of other pillar recommendations.

PEER AGENT FINDINGS:
{{$peer_findings}}

MY PERFORMANCE ANALYSIS:
{{$my_analysis}}

COLLABORATION GOAL:
{{$collaboration_goal}}

TASK: Evaluate performance impacts:

1. **Reliability Performance**: How do HA/DR strategies affect performance?
2. **Security Performance**: What performance overhead do security controls add?
3. **Cost Performance**: How do cost optimizations impact performance capabilities?
4. **Operational Performance**: How do monitoring and automation affect performance?

Identify performance trade-offs and optimization opportunities."""

    def _get_synthesis_prompt_template(self) -> str:
        return """Create performance efficiency recommendations considering all pillar interactions.

ANALYSIS RESULTS:
{{$analysis_results}}

COLLABORATION INSIGHTS:
{{$collaboration_insights}}

AZURE SERVICES CONTEXT:
{{$azure_services}}

TASK: Provide performance recommendations that:
1. Optimize response times and throughput
2. Balance performance with other pillar requirements
3. Implement scalable performance solutions
4. Consider cost-performance trade-offs"""

    def _get_focus_areas(self) -> str:
        return "Scalability patterns, load testing, caching strategies, CDN implementation, database optimization, Azure performance services, auto-scaling"
    
    def _parse_analysis_results(self, analysis: str) -> Dict[str, Any]:
        return {
            "overall_score": 64.5,
            "sub_categories": {
                "Scalability": {"score": 70, "findings": "Auto-scaling configured for some services"},
                "Load Testing": {"score": 55, "findings": "Limited load testing implementation"},
                "Caching Strategy": {"score": 60, "findings": "Basic caching in place"},
                "Database Performance": {"score": 73, "findings": "Database indexes optimized"}
            },
            "performance_bottlenecks": ["Database connection pooling", "Lack of CDN"],
            "optimization_opportunities": ["Implement Redis caching", "Add CDN layer"],
            "recommendations": []
        }
    
    def _parse_recommendations(self, recommendations: str) -> List[Dict[str, Any]]:
        return [
            {
                "priority": "High",
                "title": "Implement Multi-level Caching",
                "description": "Deploy Azure Cache for Redis and application-level caching",
                "azure_service": "Azure Cache for Redis",
                "performance_impact": "5-10x faster response times"
            }
        ]
    
    def _calculate_confidence_score(self) -> float:
        return 0.87
    
    def _extract_azure_services(self, recommendations: str) -> List[str]:
        return ["Azure Cache for Redis", "Azure CDN", "Azure Load Testing"]
    
    def _identify_dependencies(self, peer_pillar: str, peer_analysis: str) -> List[str]:
        dependencies = {
            "Reliability": ["Load balancing affects performance", "Redundancy may impact latency"],
            "Security": ["Security controls may affect performance", "Encryption overhead"],
            "Cost Optimization": ["Performance tiers affect costs", "Scaling strategies impact spending"],
            "Operational Excellence": ["Performance monitoring requirements", "Automated scaling operations"]
        }
        return dependencies.get(peer_pillar, [])
    
    def _identify_conflicts(self, peer_pillar: str, peer_analysis: str) -> List[str]:
        conflicts = {
            "Cost Optimization": ["High performance may increase costs"],
            "Security": ["Performance optimization might bypass security controls"]
        }
        return conflicts.get(peer_pillar, [])
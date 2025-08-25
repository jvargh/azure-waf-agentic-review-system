"""
Base Agent Implementation using Microsoft Semantic Kernel with A2A Protocol
Provides the foundational agent architecture for Azure Well-Architected Review
"""

import asyncio
import uuid
import json
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from datetime import datetime, timezone

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.core_plugins import MathPlugin, TimePlugin
from semantic_kernel.prompt_template import InputVariable, PromptTemplateConfig
from semantic_kernel.functions import KernelArguments

from .a2a_protocol import A2AMessage, A2AProtocol, MessageType
from .mcp_connector import MCPConnector


class BaseWellArchitectedAgent(ABC):
    """
    Base class for all Well-Architected Framework agents
    Implements Semantic Kernel integration with A2A protocol for collaboration
    """
    
    def __init__(
        self,
        agent_name: str,
        pillar_name: str,
        api_key: str,
        model: str = "gpt-4",
        agent_id: Optional[str] = None
    ):
        self.agent_name = agent_name
        self.pillar_name = pillar_name
        self.agent_id = agent_id or str(uuid.uuid4())
        self.model = model
        
        # Initialize Semantic Kernel
        self.kernel = sk.Kernel()
        
        # Add OpenAI Chat Completion service
        self.kernel.add_service(
            OpenAIChatCompletion(
                service_id="openai_chat",
                ai_model_id=model,
                api_key=api_key
            )
        )
        
        # Add core plugins
        self.kernel.add_plugin(MathPlugin(), plugin_name="MathPlugin")
        self.kernel.add_plugin(TimePlugin(), plugin_name="TimePlugin")
        
        # Initialize A2A Protocol handler
        self.a2a = A2AProtocol(self.agent_id, self.agent_name)
        
        # Initialize MCP Connector for external data sources
        self.mcp = MCPConnector()
        
        # Agent state and collaboration data
        self.collaboration_context = {}
        self.peer_agents = {}
        self.analysis_results = {}
        
        # Initialize agent-specific semantic functions
        self._initialize_semantic_functions()
    
    def _initialize_semantic_functions(self):
        """Initialize Semantic Kernel functions for this agent"""
        
        # Core analysis function
        self.analysis_function = self.kernel.add_function(
            plugin_name=f"{self.pillar_name}Plugin",
            function_name="analyze_architecture",
            prompt_template_config=PromptTemplateConfig(
                template=self._get_analysis_prompt_template(),
                input_variables=[
                    InputVariable(name="architecture_content", description="Architecture documentation to analyze"),
                    InputVariable(name="previous_findings", description="Findings from other agents", is_required=False),
                    InputVariable(name="focus_areas", description="Specific areas to focus on", is_required=False)
                ]
            )
        )
        
        # Collaboration function for agent-to-agent communication
        self.collaboration_function = self.kernel.add_function(
            plugin_name=f"{self.pillar_name}Plugin", 
            function_name="collaborate_with_peers",
            prompt_template_config=PromptTemplateConfig(
                template=self._get_collaboration_prompt_template(),
                input_variables=[
                    InputVariable(name="peer_findings", description="Findings from other agents"),
                    InputVariable(name="my_analysis", description="This agent's analysis results"),
                    InputVariable(name="collaboration_goal", description="Goal of the collaboration")
                ]
            )
        )
        
        # Recommendation synthesis function
        self.synthesis_function = self.kernel.add_function(
            plugin_name=f"{self.pillar_name}Plugin",
            function_name="synthesize_recommendations", 
            prompt_template_config=PromptTemplateConfig(
                template=self._get_synthesis_prompt_template(),
                input_variables=[
                    InputVariable(name="analysis_results", description="Complete analysis results"),
                    InputVariable(name="collaboration_insights", description="Insights from agent collaboration"),
                    InputVariable(name="azure_services", description="Available Azure services context")
                ]
            )
        )
    
    @abstractmethod
    def _get_analysis_prompt_template(self) -> str:
        """Get the analysis prompt template for this specific agent"""
        pass
    
    @abstractmethod 
    def _get_collaboration_prompt_template(self) -> str:
        """Get the collaboration prompt template for this agent"""
        pass
    
    @abstractmethod
    def _get_synthesis_prompt_template(self) -> str:
        """Get the recommendation synthesis prompt template"""
        pass
    
    async def analyze(
        self,
        architecture_content: str,
        collaboration_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform pillar-specific analysis with agent collaboration
        """
        print(f"🤖 {self.agent_name} starting analysis...")
        
        # Step 1: Gather context from MCP servers
        mcp_context = await self.mcp.get_azure_context(self.pillar_name)
        
        # Step 2: Perform initial analysis
        analysis_args = KernelArguments(
            architecture_content=architecture_content,
            previous_findings=json.dumps(collaboration_context.get("previous_findings", {}) if collaboration_context else {}),
            focus_areas=self._get_focus_areas()
        )
        
        initial_analysis = await self.analysis_function.invoke(self.kernel, analysis_args)
        
        # Step 3: Request collaboration from peer agents if available
        collaboration_results = await self._collaborate_with_peers(
            initial_analysis.value,
            collaboration_context
        )
        
        # Step 4: Synthesize final recommendations
        final_recommendations = await self._synthesize_recommendations(
            initial_analysis.value,
            collaboration_results,
            mcp_context
        )
        
        # Step 5: Format results for A2A protocol
        results = {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "pillar": self.pillar_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "analysis": self._parse_analysis_results(initial_analysis.value),
            "collaboration_insights": collaboration_results,
            "recommendations": self._parse_recommendations(final_recommendations.value),
            "confidence_score": self._calculate_confidence_score(),
            "azure_services": self._extract_azure_services(final_recommendations.value)
        }
        
        # Store results for future collaboration
        self.analysis_results = results
        
        print(f"✅ {self.agent_name} completed analysis with confidence: {results['confidence_score']}")
        return results
    
    async def _collaborate_with_peers(
        self,
        my_analysis: str,
        collaboration_context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Collaborate with peer agents using A2A protocol
        """
        if not self.peer_agents or not collaboration_context:
            return {"collaboration_notes": "No peer collaboration available"}
        
        collaboration_results = {}
        
        # Send analysis to peer agents and request feedback
        for peer_id, peer_agent in self.peer_agents.items():
            try:
                # Create A2A message
                message = A2AMessage(
                    message_type=MessageType.COLLABORATION_REQUEST,
                    sender_id=self.agent_id,
                    receiver_id=peer_id,
                    content={
                        "pillar": self.pillar_name,
                        "analysis": my_analysis,
                        "collaboration_goal": f"Review {self.pillar_name} findings for cross-pillar insights"
                    }
                )
                
                # Send via A2A protocol
                response = await self.a2a.send_message(message, peer_agent)
                
                if response and response.content:
                    collaboration_results[peer_agent.pillar_name] = response.content
                    print(f"🤝 {self.agent_name} received collaboration from {peer_agent.agent_name}")
            
            except Exception as e:
                print(f"⚠️ Collaboration failed with {peer_agent.agent_name}: {e}")
                collaboration_results[peer_agent.pillar_name] = {"error": str(e)}
        
        # Process collaboration insights using Semantic Kernel
        if collaboration_results:
            collab_args = KernelArguments(
                peer_findings=json.dumps(collaboration_results),
                my_analysis=my_analysis,
                collaboration_goal="Identify cross-pillar dependencies and conflicts"
            )
            
            enhanced_insights = await self.collaboration_function.invoke(self.kernel, collab_args)
            collaboration_results["synthesis"] = enhanced_insights.value
        
        return collaboration_results
    
    async def _synthesize_recommendations(
        self,
        analysis: str,
        collaboration_results: Dict[str, Any],
        mcp_context: Dict[str, Any]
    ) -> Any:
        """
        Synthesize final recommendations using all available context
        """
        synthesis_args = KernelArguments(
            analysis_results=analysis,
            collaboration_insights=json.dumps(collaboration_results),
            azure_services=json.dumps(mcp_context.get("azure_services", {}))
        )
        
        return await self.synthesis_function.invoke(self.kernel, synthesis_args)
    
    def register_peer_agent(self, peer_agent: 'BaseWellArchitectedAgent'):
        """Register a peer agent for collaboration via A2A protocol"""
        self.peer_agents[peer_agent.agent_id] = peer_agent
        print(f"🔗 {self.agent_name} registered peer: {peer_agent.agent_name}")
    
    async def handle_a2a_message(self, message: A2AMessage) -> A2AMessage:
        """
        Handle incoming A2A protocol messages from peer agents
        """
        try:
            if message.message_type == MessageType.COLLABORATION_REQUEST:
                # Process collaboration request
                response_content = await self._process_collaboration_request(message.content)
                
                return A2AMessage(
                    message_type=MessageType.COLLABORATION_RESPONSE,
                    sender_id=self.agent_id,
                    receiver_id=message.sender_id,
                    content=response_content
                )
            
            elif message.message_type == MessageType.NEGOTIATION:
                # Handle negotiation for conflicting recommendations
                negotiation_result = await self._negotiate_recommendations(message.content)
                
                return A2AMessage(
                    message_type=MessageType.NEGOTIATION_RESPONSE,
                    sender_id=self.agent_id,
                    receiver_id=message.sender_id,
                    content=negotiation_result
                )
            
            else:
                return A2AMessage(
                    message_type=MessageType.ERROR,
                    sender_id=self.agent_id,
                    receiver_id=message.sender_id,
                    content={"error": f"Unsupported message type: {message.message_type}"}
                )
        
        except Exception as e:
            return A2AMessage(
                message_type=MessageType.ERROR,
                sender_id=self.agent_id,
                receiver_id=message.sender_id,
                content={"error": str(e)}
            )
    
    async def _process_collaboration_request(self, request_content: Dict[str, Any]) -> Dict[str, Any]:
        """Process collaboration request from peer agent"""
        peer_pillar = request_content.get("pillar", "Unknown")
        peer_analysis = request_content.get("analysis", "")
        
        # Use Semantic Kernel to analyze peer findings for cross-pillar insights
        collab_args = KernelArguments(
            peer_findings=peer_analysis,
            my_analysis=json.dumps(self.analysis_results.get("analysis", {})),
            collaboration_goal=f"Identify {self.pillar_name} implications of {peer_pillar} findings"
        )
        
        collaboration_response = await self.collaboration_function.invoke(self.kernel, collab_args)
        
        return {
            "pillar": self.pillar_name,
            "collaboration_insights": collaboration_response.value,
            "cross_pillar_dependencies": self._identify_dependencies(peer_pillar, peer_analysis),
            "potential_conflicts": self._identify_conflicts(peer_pillar, peer_analysis)
        }
    
    async def _negotiate_recommendations(self, negotiation_content: Dict[str, Any]) -> Dict[str, Any]:
        """Negotiate conflicting recommendations with peer agents"""
        # Implement recommendation negotiation logic
        # This would use Semantic Kernel to find compromise solutions
        return {
            "negotiation_result": "compromise_reached",
            "updated_recommendations": [],
            "rationale": "Balanced approach considering both pillars"
        }
    
    @abstractmethod
    def _get_focus_areas(self) -> str:
        """Get pillar-specific focus areas"""
        pass
    
    @abstractmethod
    def _parse_analysis_results(self, analysis: str) -> Dict[str, Any]:
        """Parse and structure analysis results"""
        pass
    
    @abstractmethod
    def _parse_recommendations(self, recommendations: str) -> List[Dict[str, Any]]:
        """Parse and structure recommendations"""
        pass
    
    @abstractmethod
    def _calculate_confidence_score(self) -> float:
        """Calculate confidence score for the analysis"""
        pass
    
    @abstractmethod
    def _extract_azure_services(self, recommendations: str) -> List[str]:
        """Extract Azure services mentioned in recommendations"""
        pass
    
    @abstractmethod
    def _identify_dependencies(self, peer_pillar: str, peer_analysis: str) -> List[str]:
        """Identify cross-pillar dependencies"""
        pass
    
    @abstractmethod
    def _identify_conflicts(self, peer_pillar: str, peer_analysis: str) -> List[str]:
        """Identify potential conflicts with peer analysis"""
        pass
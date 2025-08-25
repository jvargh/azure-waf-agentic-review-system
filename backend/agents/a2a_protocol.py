"""
Agent-to-Agent (A2A) Protocol Implementation
Enables seamless communication and collaboration between Well-Architected agents
"""

import asyncio
import json
import uuid
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Any, Optional, List, TYPE_CHECKING
from datetime import datetime, timezone

# Forward reference for type hints
if TYPE_CHECKING:
    from .base_agent import BaseWellArchitectedAgent


class MessageType(Enum):
    """A2A Protocol Message Types"""
    COLLABORATION_REQUEST = "collaboration_request"
    COLLABORATION_RESPONSE = "collaboration_response" 
    NEGOTIATION = "negotiation"
    NEGOTIATION_RESPONSE = "negotiation_response"
    STATUS_UPDATE = "status_update"
    ERROR = "error"
    HEARTBEAT = "heartbeat"


@dataclass
class A2AMessage:
    """A2A Protocol Message Structure"""
    message_type: MessageType
    sender_id: str
    receiver_id: str
    content: Dict[str, Any]
    message_id: str = None
    timestamp: str = None
    correlation_id: str = None
    
    def __post_init__(self):
        if self.message_id is None:
            self.message_id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization"""
        result = asdict(self)
        result["message_type"] = self.message_type.value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'A2AMessage':
        """Create message from dictionary"""
        data["message_type"] = MessageType(data["message_type"])
        return cls(**data)


class A2AProtocol:
    """
    Agent-to-Agent Protocol Handler
    Manages communication between specialized Well-Architected agents
    """
    
    def __init__(self, agent_id: str, agent_name: str):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.message_queue = asyncio.Queue()
        self.response_handlers = {}
        self.collaboration_sessions = {}
        
    async def send_message(
        self,
        message: A2AMessage,
        target_agent: 'BaseWellArchitectedAgent'
    ) -> Optional[A2AMessage]:
        """
        Send A2A message to target agent and wait for response
        """
        try:
            print(f"📤 {self.agent_name} sending {message.message_type.value} to {target_agent.agent_name}")
            
            # Send message to target agent
            response = await target_agent.handle_a2a_message(message)
            
            if response:
                print(f"📥 {self.agent_name} received response from {target_agent.agent_name}")
                return response
            
            return None
            
        except Exception as e:
            print(f"❌ A2A message failed from {self.agent_name} to {target_agent.agent_name}: {e}")
            return A2AMessage(
                message_type=MessageType.ERROR,
                sender_id=self.agent_id,
                receiver_id=target_agent.agent_id,
                content={"error": str(e)}
            )
    
    async def broadcast_message(
        self,
        message: A2AMessage,
        target_agents: List['BaseWellArchitectedAgent']
    ) -> Dict[str, A2AMessage]:
        """
        Broadcast message to multiple agents
        """
        responses = {}
        
        # Send to all agents concurrently
        tasks = [
            self.send_message(message, agent)
            for agent in target_agents
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            agent_name = target_agents[i].agent_name
            if isinstance(result, Exception):
                responses[agent_name] = A2AMessage(
                    message_type=MessageType.ERROR,
                    sender_id=self.agent_id,
                    receiver_id=target_agents[i].agent_id,
                    content={"error": str(result)}
                )
            else:
                responses[agent_name] = result
        
        return responses
    
    async def initiate_collaboration_session(
        self,
        session_topic: str,
        participating_agents: List['BaseWellArchitectedAgent'],
        session_data: Dict[str, Any]
    ) -> str:
        """
        Initiate a multi-agent collaboration session
        """
        session_id = str(uuid.uuid4())
        
        self.collaboration_sessions[session_id] = {
            "topic": session_topic,
            "participants": [agent.agent_id for agent in participating_agents],
            "session_data": session_data,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "active"
        }
        
        # Notify all participants about the session
        session_message = A2AMessage(
            message_type=MessageType.COLLABORATION_REQUEST,
            sender_id=self.agent_id,
            receiver_id="broadcast",
            content={
                "session_id": session_id,
                "topic": session_topic,
                "session_data": session_data,
                "action": "join_session"
            },
            correlation_id=session_id
        )
        
        responses = await self.broadcast_message(session_message, participating_agents)
        
        print(f"🎯 Collaboration session '{session_topic}' initiated with {len(participating_agents)} agents")
        
        return session_id
    
    async def negotiate_recommendations(
        self,
        conflicting_recommendations: Dict[str, Any],
        involved_agents: List['BaseWellArchitectedAgent']
    ) -> Dict[str, Any]:
        """
        Facilitate negotiation between agents with conflicting recommendations
        """
        negotiation_id = str(uuid.uuid4())
        
        print(f"⚖️ Starting recommendation negotiation between {len(involved_agents)} agents")
        
        # Round 1: Present conflicts and gather positions
        negotiation_message = A2AMessage(
            message_type=MessageType.NEGOTIATION,
            sender_id=self.agent_id,
            receiver_id="broadcast",
            content={
                "negotiation_id": negotiation_id,
                "conflicts": conflicting_recommendations,
                "action": "present_position",
                "round": 1
            },
            correlation_id=negotiation_id
        )
        
        round1_responses = await self.broadcast_message(negotiation_message, involved_agents)
        
        # Round 2: Seek compromise based on positions
        positions = {
            agent_name: response.content
            for agent_name, response in round1_responses.items()
            if response and response.message_type != MessageType.ERROR
        }
        
        compromise_message = A2AMessage(
            message_type=MessageType.NEGOTIATION,
            sender_id=self.agent_id,
            receiver_id="broadcast",
            content={
                "negotiation_id": negotiation_id,
                "all_positions": positions,
                "action": "find_compromise",
                "round": 2
            },
            correlation_id=negotiation_id
        )
        
        round2_responses = await self.broadcast_message(compromise_message, involved_agents)
        
        # Synthesize final negotiated recommendations
        negotiated_result = self._synthesize_negotiation_results(
            conflicting_recommendations,
            positions,
            round2_responses
        )
        
        print(f"✅ Negotiation completed: {negotiated_result.get('outcome', 'unknown')}")
        
        return negotiated_result
    
    def _synthesize_negotiation_results(
        self,
        original_conflicts: Dict[str, Any],
        agent_positions: Dict[str, Any],
        compromise_responses: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesize the final negotiated recommendations
        """
        # Simple synthesis logic - in production this could use LLM reasoning
        compromises = []
        
        for agent_name, response in compromise_responses.items():
            if (response and 
                response.message_type != MessageType.ERROR and 
                "compromise" in response.content):
                compromises.append(response.content["compromise"])
        
        return {
            "negotiation_outcome": "resolved" if compromises else "unresolved",
            "original_conflicts": original_conflicts,
            "agent_positions": agent_positions,
            "negotiated_recommendations": compromises,
            "consensus_level": len(compromises) / len(agent_positions) if agent_positions else 0,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def get_collaboration_metrics(self) -> Dict[str, Any]:
        """
        Get metrics about agent collaboration effectiveness
        """
        active_sessions = sum(
            1 for session in self.collaboration_sessions.values()
            if session["status"] == "active"
        )
        
        return {
            "total_sessions": len(self.collaboration_sessions),
            "active_sessions": active_sessions,
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "message_queue_size": self.message_queue.qsize()
        }
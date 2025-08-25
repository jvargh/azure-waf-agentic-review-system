"""
Performance Monitoring and Analytics for Azure Well-Architected Review System
Tracks system performance, agent collaboration metrics, and analysis quality
"""

import asyncio
import json
import time
from typing import Dict, Any, List
from datetime import datetime, timezone
from collections import defaultdict


class PerformanceMonitor:
    """
    Advanced performance monitoring for the multi-agent system
    Tracks analysis speed, collaboration efficiency, and recommendation quality
    """
    
    def __init__(self):
        self.metrics = {
            "analysis_performance": [],
            "agent_collaboration": [],
            "recommendation_quality": [],
            "system_health": [],
            "user_satisfaction": []
        }
        
        self.real_time_stats = {
            "active_analyses": 0,
            "total_assessments": 0,
            "average_analysis_time": 0,
            "agent_success_rate": 0,
            "recommendation_acceptance_rate": 0
        }
    
    async def start_analysis_tracking(self, assessment_id: str, assessment_name: str) -> str:
        """Start tracking performance for a new analysis"""
        
        tracking_id = f"track_{assessment_id}_{int(time.time())}"
        
        tracking_data = {
            "tracking_id": tracking_id,
            "assessment_id": assessment_id,
            "assessment_name": assessment_name,
            "start_time": time.time(),
            "start_timestamp": datetime.now(timezone.utc).isoformat(),
            "phases": {
                "initialization": {"start": time.time(), "duration": 0},
                "image_analysis": {"start": 0, "duration": 0},
                "reactive_analysis": {"start": 0, "duration": 0},
                "agent_analysis": {"start": 0, "duration": 0, "agent_times": {}},
                "collaboration": {"start": 0, "duration": 0, "messages": 0},
                "synthesis": {"start": 0, "duration": 0}
            },
            "agent_performance": {},
            "collaboration_metrics": {
                "a2a_messages": 0,
                "successful_collaborations": 0,
                "failed_collaborations": 0,
                "consensus_reached": 0
            },
            "quality_metrics": {
                "recommendations_generated": 0,
                "high_priority_recommendations": 0,
                "cross_pillar_insights": 0,
                "image_insights": 0,
                "reactive_insights": 0
            }
        }
        
        self.metrics["analysis_performance"].append(tracking_data)
        self.real_time_stats["active_analyses"] += 1
        
        print(f"📊 Performance tracking started for: {assessment_name}")
        return tracking_id
    
    async def track_phase_completion(self, tracking_id: str, phase: str, **kwargs):
        """Track completion of analysis phase"""
        
        current_time = time.time()
        
        for tracking_data in self.metrics["analysis_performance"]:
            if tracking_data["tracking_id"] == tracking_id:
                if phase in tracking_data["phases"]:
                    if tracking_data["phases"][phase]["start"] == 0:
                        tracking_data["phases"][phase]["start"] = current_time
                    
                    tracking_data["phases"][phase]["duration"] = current_time - tracking_data["phases"][phase]["start"]
                    
                    # Track specific phase metrics
                    if phase == "agent_analysis" and "agent_times" in kwargs:
                        tracking_data["phases"][phase]["agent_times"] = kwargs["agent_times"]
                    
                    elif phase == "collaboration" and "messages_count" in kwargs:
                        tracking_data["collaboration_metrics"]["a2a_messages"] = kwargs["messages_count"]
                    
                    print(f"⏱️ Phase '{phase}' completed in {tracking_data['phases'][phase]['duration']:.2f}s")
                    break
    
    async def track_agent_performance(self, tracking_id: str, agent_name: str, performance_data: Dict[str, Any]):
        """Track individual agent performance"""
        
        for tracking_data in self.metrics["analysis_performance"]:
            if tracking_data["tracking_id"] == tracking_id:
                tracking_data["agent_performance"][agent_name] = {
                    "analysis_time": performance_data.get("analysis_time", 0),
                    "confidence_score": performance_data.get("confidence_score", 0),
                    "recommendations_count": len(performance_data.get("recommendations", [])),
                    "collaboration_messages": performance_data.get("collaboration_messages", 0),
                    "success": performance_data.get("success", True)
                }
                break
    
    async def complete_analysis_tracking(self, tracking_id: str, final_results: Dict[str, Any]):
        """Complete analysis tracking and calculate final metrics"""
        
        completion_time = time.time()
        
        for tracking_data in self.metrics["analysis_performance"]:
            if tracking_data["tracking_id"] == tracking_id:
                # Calculate total analysis time
                total_time = completion_time - tracking_data["start_time"]
                tracking_data["total_duration"] = total_time
                tracking_data["completion_timestamp"] = datetime.now(timezone.utc).isoformat()
                
                # Update quality metrics
                recommendations = final_results.get("recommendations", [])
                tracking_data["quality_metrics"]["recommendations_generated"] = len(recommendations)
                tracking_data["quality_metrics"]["high_priority_recommendations"] = len([
                    r for r in recommendations if r.get("priority") in ["Critical", "High"]
                ])
                
                # Update collaboration metrics
                collab_metrics = final_results.get("collaboration_metrics", {})
                tracking_data["collaboration_metrics"].update(collab_metrics)
                
                # Update real-time stats
                self.real_time_stats["active_analyses"] -= 1
                self.real_time_stats["total_assessments"] += 1
                
                # Calculate running averages
                all_durations = [t["total_duration"] for t in self.metrics["analysis_performance"] 
                               if "total_duration" in t]
                if all_durations:
                    self.real_time_stats["average_analysis_time"] = sum(all_durations) / len(all_durations)
                
                print(f"✅ Analysis tracking completed in {total_time:.2f}s with {len(recommendations)} recommendations")
                
                return tracking_data
        
        return None
    
    def get_performance_analytics(self) -> Dict[str, Any]:
        """Get comprehensive performance analytics"""
        
        completed_analyses = [t for t in self.metrics["analysis_performance"] if "total_duration" in t]
        
        if not completed_analyses:
            return {"message": "No completed analyses available for analytics"}
        
        # Calculate performance statistics
        durations = [t["total_duration"] for t in completed_analyses]
        recommendation_counts = [t["quality_metrics"]["recommendations_generated"] for t in completed_analyses]
        
        # Agent performance analysis
        agent_stats = defaultdict(list)
        for analysis in completed_analyses:
            for agent_name, perf in analysis["agent_performance"].items():
                agent_stats[agent_name].append(perf)
        
        agent_performance = {}
        for agent_name, perfs in agent_stats.items():
            if perfs:
                agent_performance[agent_name] = {
                    "average_analysis_time": sum(p["analysis_time"] for p in perfs) / len(perfs),
                    "average_confidence": sum(p["confidence_score"] for p in perfs) / len(perfs),
                    "total_recommendations": sum(p["recommendations_count"] for p in perfs),
                    "success_rate": sum(1 for p in perfs if p["success"]) / len(perfs) * 100
                }
        
        # Collaboration efficiency
        total_messages = sum(t["collaboration_metrics"]["a2a_messages"] for t in completed_analyses)
        successful_collabs = sum(t["collaboration_metrics"]["successful_collaborations"] for t in completed_analyses)
        
        return {
            "overall_performance": {
                "total_assessments_completed": len(completed_analyses),
                "average_analysis_time": sum(durations) / len(durations),
                "fastest_analysis": min(durations),
                "slowest_analysis": max(durations),
                "average_recommendations_per_analysis": sum(recommendation_counts) / len(recommendation_counts)
            },
            "agent_performance": agent_performance,
            "collaboration_metrics": {
                "total_a2a_messages": total_messages,
                "successful_collaborations": successful_collabs,
                "collaboration_efficiency": successful_collabs / max(total_messages, 1) * 100
            },
            "quality_metrics": {
                "high_priority_recommendation_rate": sum(
                    t["quality_metrics"]["high_priority_recommendations"] for t in completed_analyses
                ) / sum(recommendation_counts) * 100 if sum(recommendation_counts) > 0 else 0
            },
            "real_time_stats": self.real_time_stats,
            "system_health": self._calculate_system_health()
        }
    
    def _calculate_system_health(self) -> Dict[str, Any]:
        """Calculate overall system health metrics"""
        
        completed_analyses = [t for t in self.metrics["analysis_performance"] if "total_duration" in t]
        
        if not completed_analyses:
            return {"status": "initializing", "score": 0}
        
        # Calculate health score based on various factors
        recent_analyses = completed_analyses[-10:]  # Last 10 analyses
        
        # Performance health (based on analysis times)
        avg_time = sum(t["total_duration"] for t in recent_analyses) / len(recent_analyses)
        performance_score = max(0, 100 - (avg_time - 10) * 2)  # Penalty for times > 10s
        
        # Quality health (based on recommendations)
        avg_recommendations = sum(
            t["quality_metrics"]["recommendations_generated"] for t in recent_analyses
        ) / len(recent_analyses)
        quality_score = min(100, avg_recommendations * 10)  # 10 points per recommendation
        
        # Collaboration health (based on A2A success)
        total_messages = sum(t["collaboration_metrics"]["a2a_messages"] for t in recent_analyses)
        successful_collabs = sum(t["collaboration_metrics"]["successful_collaborations"] for t in recent_analyses)
        collaboration_score = (successful_collabs / max(total_messages, 1)) * 100
        
        # Overall health score
        overall_score = (performance_score + quality_score + collaboration_score) / 3
        
        health_status = "excellent" if overall_score >= 80 else "good" if overall_score >= 60 else "fair" if overall_score >= 40 else "poor"
        
        return {
            "status": health_status,
            "overall_score": round(overall_score, 1),
            "performance_score": round(performance_score, 1),
            "quality_score": round(quality_score, 1),
            "collaboration_score": round(collaboration_score, 1),
            "recent_analyses_count": len(recent_analyses)
        }
    
    def get_agent_leaderboard(self) -> List[Dict[str, Any]]:
        """Get agent performance leaderboard"""
        
        analytics = self.get_performance_analytics()
        agent_performance = analytics.get("agent_performance", {})
        
        leaderboard = []
        for agent_name, stats in agent_performance.items():
            leaderboard.append({
                "agent_name": agent_name,
                "success_rate": stats["success_rate"],
                "average_confidence": stats["average_confidence"],
                "recommendations_generated": stats["total_recommendations"],
                "efficiency_score": (stats["success_rate"] + stats["average_confidence"]) / 2
            })
        
        # Sort by efficiency score
        leaderboard.sort(key=lambda x: x["efficiency_score"], reverse=True)
        
        return leaderboard
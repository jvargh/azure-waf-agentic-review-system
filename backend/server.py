from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import base64
import asyncio
import json

# Import the simplified multi-agent system
from agents.simplified_agent_system import WellArchitectedOrchestrator

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Global orchestrator instance
orchestrator = None

# AI Analysis Functions for Real LLM Mode
async def analyze_architecture_document(content: str, filename: str) -> Dict[str, Any]:
    """Analyze architecture document content using AI"""
    if not orchestrator or not orchestrator.openai_client:
        return None
    
    try:
        prompt = f"""
        Analyze this architecture document for Azure Well-Architected Framework insights:
        
        Document: {filename}
        Content: {content[:1500]}...
        
        Provide insights on:
        1. Architecture patterns identified
        2. Potential Well-Architected Framework concerns
        3. Key components and services mentioned
        4. Recommendations for improvement
        
        Return as JSON with keys: patterns, concerns, components, recommendations
        """
        
        response = await orchestrator.openai_client.chat.completions.create(
            model=orchestrator.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        result = response.choices[0].message.content
        # Try to parse as JSON, fallback to text if needed
        try:
            return json.loads(result)
        except:
            return {"analysis": result, "filename": filename}
            
    except Exception as e:
        print(f"Architecture document analysis failed: {e}")
        return None

async def analyze_case_data(csv_content: str, filename: str) -> Dict[str, Any]:
    """Analyze CSV case data using AI"""
    if not orchestrator or not orchestrator.openai_client:
        return None
    
    try:
        # Get first few rows for analysis
        lines = csv_content.split('\n')[:10]
        sample_data = '\n'.join(lines)
        
        prompt = f"""
        Analyze this support case CSV data for patterns and insights:
        
        File: {filename}
        Sample Data:
        {sample_data}
        
        Identify:
        1. Common issue patterns
        2. Service areas with most issues
        3. Potential Well-Architected Framework violations
        4. Risk indicators
        
        Return as JSON with keys: patterns, services, violations, risks
        """
        
        response = await orchestrator.openai_client.chat.completions.create(
            model=orchestrator.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        result = response.choices[0].message.content
        try:
            return json.loads(result)
        except:
            return {"analysis": result, "filename": filename}
            
    except Exception as e:
        print(f"Case data analysis failed: {e}")
        return None

# Utility functions for MongoDB serialization
def prepare_for_mongo(data):
    """Convert datetime objects to ISO strings for MongoDB storage"""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
            elif isinstance(value, dict):
                data[key] = prepare_for_mongo(value)
            elif isinstance(value, list):
                data[key] = [prepare_for_mongo(item) if isinstance(item, dict) else item for item in value]
    return data

def parse_from_mongo(item):
    """Parse datetime strings back from MongoDB"""
    if isinstance(item, dict):
        for key, value in item.items():
            if key.endswith('_at') or key == 'timestamp':
                if isinstance(value, str):
                    try:
                        item[key] = datetime.fromisoformat(value)
                    except:
                        pass
            elif isinstance(value, dict):
                item[key] = parse_from_mongo(value)
            elif isinstance(value, list):
                item[key] = [parse_from_mongo(i) if isinstance(i, dict) else i for i in value]
    return item

# Models
class DocumentUpload(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    content_type: str
    file_base64: str
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ai_insights: Optional[Dict[str, Any]] = None

class PillarScore(BaseModel):
    pillar_name: str
    overall_score: float
    max_score: float
    percentage: float
    sub_categories: Dict[str, Dict[str, float]]  # category -> {score, max_score, percentage}

class Recommendation(BaseModel):
    pillar: str
    category: str
    priority: str  # High, Medium, Low
    title: str
    description: str
    impact: str
    effort: str  # High, Medium, Low
    azure_service: Optional[str] = None
    reference_url: Optional[str] = None

class Assessment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    documents: List[DocumentUpload] = []
    status: str = "pending"  # pending, analyzing, completed, failed
    progress: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    pillar_scores: List[PillarScore] = []
    recommendations: List[Recommendation] = []
    overall_score: Optional[float] = None
    overall_percentage: Optional[float] = None
    # New fields for agent system
    agent_metrics: Optional[Dict[str, Any]] = None
    collaboration_metrics: Optional[Dict[str, Any]] = None
    # Reactive analysis fields
    reactive_cases_csv: Optional[str] = None
    reactive_analysis_results: Optional[Dict[str, Any]] = None
    # Current system configuration
    llm_mode: Optional[str] = None

class AssessmentCreate(BaseModel):
    name: str
    description: Optional[str] = None

class AssessmentResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: str
    progress: int
    created_at: datetime
    completed_at: Optional[datetime]
    document_count: int
    overall_score: Optional[float]
    overall_percentage: Optional[float]

# Initialize orchestrator with enhanced configuration options
def initialize_orchestrator():
    global orchestrator
    api_key = os.environ.get('OPENAI_API_KEY', 'mock-key')
    model = os.environ.get('LLM_MODEL', 'gpt-4')
    llm_mode = os.environ.get('LLM_MODE', 'emulated')  # 'emulated' or 'real'
    
    try:
        orchestrator = WellArchitectedOrchestrator(api_key, model, llm_mode)
        
        if llm_mode == 'emulated':
            print("🤖 Multi-agent orchestrator initialized in ENHANCED EMULATED mode")
            print("   🎭 Framework: Advanced Emulation System with A2A Protocol")
            print("   🔧 Features: Realistic AI responses with sophisticated analysis")
            print("   🤝 Agents: 5 specialized Well-Architected experts")
            print("   🌐 Collaboration: Autonomous cross-pillar analysis")
            print("   🚀 Ready for future GPT-5 integration")
        else:
            print("🤖 Multi-agent orchestrator initialized in REAL LLM mode")
            print(f"   🔧 Model: {model}")
            print("   🤝 Agents: 5 specialized Well-Architected experts with real AI")
            print("   🌐 Collaboration: Live Agent-to-Agent protocol")
            
    except Exception as e:
        print(f"⚠️ Failed to initialize orchestrator: {e}")
        orchestrator = None

# Progress callback for real-time updates
async def update_progress(assessment_id: str, progress: int, status_message: str):
    """Update assessment progress in database"""
    try:
        await db.assessments.update_one(
            {"id": assessment_id},
            {
                "$set": {
                    "progress": progress,
                    "status": "analyzing" if progress < 100 else "completed"
                }
            }
        )
        print(f"📊 {assessment_id}: {progress}% - {status_message}")
    except Exception as e:
        print(f"❌ Progress update failed: {e}")

# Multi-agent analysis process
async def conduct_agent_analysis(assessment_id: str):
    """Conduct comprehensive analysis using multi-agent system"""
    try:
        # Fetch assessment data
        assessment = await db.assessments.find_one({"id": assessment_id})
        if not assessment:
            print(f"❌ Assessment {assessment_id} not found")
            return
        
        # Extract architecture content from documents
        architecture_content = ""
        documents_list = []
        
        for doc in assessment.get("documents", []):
            try:
                # Store document info for image analysis
                documents_list.append({
                    "filename": doc["filename"],
                    "content_type": doc["content_type"],
                    "file_base64": doc["file_base64"]
                })
                
                # Decode text content for non-image files
                if not doc["content_type"].startswith("image/"):
                    content_bytes = base64.b64decode(doc["file_base64"])
                    content_text = content_bytes.decode('utf-8', errors='ignore')
                    architecture_content += f"\n\n--- {doc['filename']} ---\n{content_text[:2000]}"
                    
            except Exception as e:
                print(f"⚠️ Failed to process document {doc.get('filename', 'unknown')}: {e}")
        
        if not architecture_content.strip():
            architecture_content = f"""
            Architecture Review for: {assessment['name']}
            
            Description: {assessment.get('description', 'No description provided')}
            
            This is a comprehensive Azure Well-Architected Framework review focusing on:
            - Reliability and availability patterns
            - Security controls and compliance
            - Cost optimization strategies  
            - Operational excellence practices
            - Performance efficiency measures
            """
        
        # Get reactive cases CSV if available
        reactive_cases_csv = assessment.get("reactive_cases_csv")
        
        if orchestrator:
            print(f"🚀 Starting enhanced multi-agent analysis for: {assessment['name']}")
            
            # Create progress callback
            progress_callback = lambda progress, message: update_progress(assessment_id, progress, message)
            
            # Conduct comprehensive review with enhanced capabilities
            results = await orchestrator.conduct_comprehensive_review(
                assessment_id=assessment_id,
                architecture_content=architecture_content,
                assessment_name=assessment['name'],
                progress_callback=progress_callback,
                documents=documents_list,
                reactive_cases_csv=reactive_cases_csv
            )
            
            # Update assessment with results
            update_data = {
                "status": "completed",
                "progress": 100,
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "overall_score": results["overall_score"],
                "overall_percentage": results["overall_percentage"],
                "pillar_scores": [prepare_for_mongo(ps) for ps in results["pillar_scores"]],
                "recommendations": [prepare_for_mongo(rec) for rec in results["recommendations"]],
                "agent_metrics": results.get("agent_performance", {}),
                "collaboration_metrics": results.get("collaboration_metrics", {})
            }
            
            await db.assessments.update_one(
                {"id": assessment_id},
                {"$set": update_data}
            )
            
            print(f"✅ Multi-agent analysis completed: {results['overall_percentage']}%")
        
        else:
            # Fallback to mock analysis if orchestrator not available
            print(f"⚠️ Using fallback mock analysis for: {assessment['name']}")
            await fallback_mock_analysis(assessment_id)
    
    except Exception as e:
        print(f"❌ Agent analysis failed for {assessment_id}: {e}")
        # Update status to failed
        await db.assessments.update_one(
            {"id": assessment_id},
            {"$set": {"status": "failed", "progress": 0}}
        )

async def fallback_mock_analysis(assessment_id: str):
    """Fallback mock analysis if agent system is not available"""
    from datetime import datetime, timezone
    
    # Mock pillar scores
    pillar_scores = [
        {
            "pillar_name": "Reliability",
            "overall_score": 72.5,
            "max_score": 100,
            "percentage": 72.5,
            "sub_categories": {
                "High Availability": {"score": 80, "max_score": 100, "percentage": 80},
                "Disaster Recovery": {"score": 65, "max_score": 100, "percentage": 65}
            }
        },
        {
            "pillar_name": "Security", 
            "overall_score": 68.0,
            "max_score": 100,
            "percentage": 68.0,
            "sub_categories": {
                "Identity & Access": {"score": 75, "max_score": 100, "percentage": 75},
                "Data Protection": {"score": 60, "max_score": 100, "percentage": 60}
            }
        }
    ]
    
    # Mock recommendations
    recommendations = [
        {
            "pillar": "Reliability",
            "category": "High Availability", 
            "priority": "High",
            "title": "Implement Multi-Region Deployment",
            "description": "Deploy applications across multiple Azure regions",
            "impact": "Significantly improves availability",
            "effort": "High",
            "azure_service": "Azure Traffic Manager"
        }
    ]
    
    # Simulate analysis progression
    for i in range(5):
        progress = (i + 1) * 20
        await update_progress(assessment_id, progress, f"Mock analysis step {i+1}")
        await asyncio.sleep(2)
    
    # Update with final results
    overall_score = sum(ps["overall_score"] for ps in pillar_scores) / len(pillar_scores)
    
    update_data = {
        "status": "completed",
        "progress": 100,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "overall_score": round(overall_score, 1),
        "overall_percentage": round(overall_score, 1),
        "pillar_scores": pillar_scores,
        "recommendations": recommendations,
        "agent_metrics": {"mock_mode": True},
        "collaboration_metrics": {"mock_mode": True}
    }
    
    await db.assessments.update_one(
        {"id": assessment_id},
        {"$set": update_data}
    )

# Routes
@api_router.get("/")
async def root():
    llm_mode = os.environ.get('LLM_MODE', 'emulated')
    return {
        "message": "Azure Well-Architected Review API - Enhanced Multi-Agent System",
        "agent_system": "Enhanced Emulated Mode" if llm_mode == 'emulated' else "Real LLM Mode" if orchestrator else "Mock Mode",
        "llm_mode": llm_mode,
        "ai_framework": "Microsoft Semantic Kernel + Enhanced A2A Protocol",
        "capabilities": {
            "image_analysis": "Architecture diagram analysis enabled",
            "reactive_case_analysis": "Support case pattern analysis enabled", 
            "enhanced_emulation": "Sophisticated AI response simulation" if llm_mode == 'emulated' else None,
            "future_ready": "GPT-5 integration ready"
        },
        "version": "2.1.0-enhanced"
    }

@api_router.post("/assessments", response_model=Assessment)
async def create_assessment(assessment_data: AssessmentCreate):
    assessment = Assessment(**assessment_data.dict())
    # Set current system configuration
    assessment.llm_mode = os.environ.get('LLM_MODE', 'emulated')
    assessment_dict = prepare_for_mongo(assessment.dict())
    await db.assessments.insert_one(assessment_dict)
    return assessment

@api_router.get("/assessments", response_model=List[AssessmentResponse])
async def get_assessments():
    assessments = await db.assessments.find().to_list(100)
    return [
        AssessmentResponse(
            id=a["id"],
            name=a["name"],
            description=a.get("description"),
            status=a["status"],
            progress=a["progress"],
            created_at=datetime.fromisoformat(a["created_at"]) if isinstance(a["created_at"], str) else a["created_at"],
            completed_at=datetime.fromisoformat(a["completed_at"]) if a.get("completed_at") and isinstance(a["completed_at"], str) else a.get("completed_at"),
            document_count=len(a.get("documents", [])),
            overall_score=a.get("overall_score"),
            overall_percentage=a.get("overall_percentage")
        ) for a in assessments
    ]

@api_router.get("/assessments/{assessment_id}", response_model=Assessment)
async def get_assessment(assessment_id: str):
    assessment = await db.assessments.find_one({"id": assessment_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Add backward compatibility for existing assessments without llm_mode
    if 'llm_mode' not in assessment:
        assessment['llm_mode'] = os.environ.get('LLM_MODE', 'emulated')
    
    return Assessment(**parse_from_mongo(assessment))

@api_router.delete("/assessments/{assessment_id}")
async def delete_assessment(assessment_id: str):
    # Check if assessment exists
    assessment = await db.assessments.find_one({"id": assessment_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Delete associated documents from database
    await db.documents.delete_many({"assessment_id": assessment_id})
    
    # Delete the assessment
    result = await db.assessments.delete_one({"id": assessment_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    return {"message": "Assessment deleted successfully", "deleted_id": assessment_id}

@api_router.post("/assessments/{assessment_id}/documents")
async def upload_document(assessment_id: str, file: UploadFile = File(...)):
    # Check if assessment exists
    assessment = await db.assessments.find_one({"id": assessment_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Read file content and encode as base64
    content = await file.read()
    file_base64 = base64.b64encode(content).decode('utf-8')
    
    # Analyze content immediately if in real LLM mode
    ai_insights = None
    llm_mode = os.environ.get('LLM_MODE', 'emulated')
    
    if llm_mode == "real" and orchestrator and orchestrator.openai_client:
        try:
            # Decode content for AI analysis
            if file.content_type == "text/plain" or file.filename.lower().endswith('.txt'):
                text_content = content.decode('utf-8')
                ai_insights = await analyze_architecture_document(text_content, file.filename)
                
            elif file.content_type == "text/csv" or file.filename.lower().endswith('.csv'):
                csv_content = content.decode('utf-8')
                ai_insights = await analyze_case_data(csv_content, file.filename)
                
        except Exception as e:
            print(f"AI analysis failed for {file.filename}: {e}")
    
    # Create document upload record with AI insights
    document = DocumentUpload(
        filename=file.filename,
        content_type=file.content_type,
        file_base64=file_base64
    )
    
    # Add AI insights to document if available
    document_dict = document.dict()
    if ai_insights:
        document_dict["ai_insights"] = ai_insights
    
    # Add document to assessment
    await db.assessments.update_one(
        {"id": assessment_id},
        {"$push": {"documents": prepare_for_mongo(document_dict)}}
    )
    
    # If it's a CSV file, also process it for reactive analysis
    if (file.content_type == "text/csv" or 
        file.filename.lower().endswith('.csv')):
        
        try:
            # Decode CSV content for analysis
            csv_text = content.decode('utf-8')
            
            # Store CSV content in assessment for analysis
            await db.assessments.update_one(
                {"id": assessment_id},
                {"$set": {"reactive_cases_csv": csv_text}}
            )
            
            # If orchestrator available, run reactive analysis
            if orchestrator:
                reactive_results = await orchestrator.case_analyzer.analyze_support_cases(csv_text)
                
                # Store reactive analysis results
                await db.assessments.update_one(
                    {"id": assessment_id},
                    {"$set": {"reactive_analysis_results": prepare_for_mongo(reactive_results)}}
                )
                
                response_data = {
                    "message": "Document uploaded and reactive analysis completed",
                    "document_id": document.id,
                    "reactive_analysis": {
                        "cases_analyzed": reactive_results.get("analysis_summary", {}).get("total_cases", 0),
                        "patterns_identified": reactive_results.get("analysis_summary", {}).get("patterns_identified", 0),
                        "wa_violations": reactive_results.get("analysis_summary", {}).get("wa_violations", 0),
                        "risk_level": reactive_results.get("risk_assessment", {}).get("risk_level", "Unknown")
                    }
                }
                
                # Add AI insights to response if available
                if ai_insights:
                    response_data["ai_insights"] = ai_insights
                
                return response_data
            else:
                response_data = {
                    "message": "CSV document uploaded successfully",
                    "document_id": document.id,
                    "note": "Reactive analysis will be processed during assessment analysis"
                }
                
                if ai_insights:
                    response_data["ai_insights"] = ai_insights
                
                return response_data
        except Exception as e:
            print(f"CSV processing failed: {e}")
            # Still return success for document upload even if CSV processing fails
            response_data = {
                "message": "Document uploaded successfully (CSV processing pending)",
                "document_id": document.id
            }
            
            if ai_insights:
                response_data["ai_insights"] = ai_insights
            
            return response_data
    
    response_data = {"message": "Document uploaded successfully", "document_id": document.id}
    if ai_insights:
        response_data["ai_insights"] = ai_insights
    
    return response_data

@api_router.post("/assessments/{assessment_id}/analyze")
async def start_analysis(assessment_id: str):
    # Check if assessment exists
    assessment = await db.assessments.find_one({"id": assessment_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    if assessment["status"] != "pending":
        raise HTTPException(status_code=400, detail="Assessment already analyzed or in progress")
    
    # Start multi-agent analysis process (run in background)
    asyncio.create_task(conduct_agent_analysis(assessment_id))
    
    return {
        "message": "Enhanced multi-agent analysis started",
        "status": "analyzing",
        "agents_deployed": len(orchestrator.agents) if orchestrator else 0,
        "capabilities": {
            "image_analysis": "Architecture diagram analysis enabled",
            "reactive_case_analysis": "Support case pattern analysis enabled",
            "a2a_collaboration": "Agent-to-Agent protocol active"
        },
        "ai_framework": "Microsoft Semantic Kernel + Enhanced Multi-Agent System"
    }

@api_router.post("/assessments/{assessment_id}/reactive-analysis")
async def upload_reactive_cases(assessment_id: str, file: UploadFile = File(...)):
    """Upload CSV file with support cases for reactive analysis"""
    
    # Check if assessment exists
    assessment = await db.assessments.find_one({"id": assessment_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Read CSV content
    csv_content = await file.read()
    csv_text = csv_content.decode('utf-8')
    
    try:
        # Store CSV content in assessment for analysis
        await db.assessments.update_one(
            {"id": assessment_id},
            {"$set": {"reactive_cases_csv": csv_text}}
        )
        
        # If orchestrator available, run reactive analysis
        if orchestrator:
            reactive_results = await orchestrator.case_analyzer.analyze_support_cases(csv_text)
            
            # Store reactive analysis results
            await db.assessments.update_one(
                {"id": assessment_id},
                {"$set": {"reactive_analysis_results": prepare_for_mongo(reactive_results)}}
            )
            
            return {
                "message": "Reactive case analysis completed",
                "cases_analyzed": reactive_results.get("analysis_summary", {}).get("total_cases", 0),
                "patterns_identified": reactive_results.get("analysis_summary", {}).get("patterns_identified", 0),
                "wa_violations": reactive_results.get("analysis_summary", {}).get("wa_violations", 0),
                "risk_level": reactive_results.get("risk_assessment", {}).get("risk_level", "Unknown")
            }
        else:
            return {"message": "Reactive cases uploaded successfully", "status": "stored"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reactive analysis failed: {str(e)}")

@api_router.get("/assessments/{assessment_id}/reactive-analysis")
async def get_reactive_analysis(assessment_id: str):
    """Get reactive case analysis results"""
    
    assessment = await db.assessments.find_one({"id": assessment_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    reactive_results = assessment.get("reactive_analysis_results")
    if not reactive_results:
        return {"message": "No reactive analysis available", "status": "not_analyzed"}
    
    return parse_from_mongo(reactive_results)

@api_router.get("/assessments/{assessment_id}/scorecard")
async def get_scorecard(assessment_id: str):
    assessment = await db.assessments.find_one({"id": assessment_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    if assessment["status"] != "completed":
        return {
            "message": "Assessment not completed yet", 
            "status": assessment["status"],
            "progress": assessment.get("progress", 0)
        }
    
    # Parse the assessment data
    parsed_assessment = parse_from_mongo(assessment)
    
    return {
        "assessment_id": assessment_id,
        "assessment_name": assessment["name"],
        "overall_score": assessment.get("overall_score"),
        "overall_percentage": assessment.get("overall_percentage"),
        "pillar_scores": parsed_assessment["pillar_scores"],
        "recommendations": parsed_assessment["recommendations"],
        "completed_at": assessment.get("completed_at"),
        # New agent system metrics
        "agent_metrics": assessment.get("agent_metrics", {}),
        "collaboration_metrics": assessment.get("collaboration_metrics", {}),
        "ai_framework": "Microsoft Semantic Kernel with A2A Protocol"
    }

@api_router.get("/system/agents")
async def get_agent_status():
    """Get status of the multi-agent system"""
    if not orchestrator:
        return {
            "status": "unavailable",
            "message": "Agent system not initialized",
            "mode": "mock_fallback"
        }
    
    agent_status = {}
    for pillar_name, agent in orchestrator.agents.items():
        agent_status[pillar_name] = {
            "agent_id": agent.agent_id,
            "agent_name": agent.agent_name,
            "pillar": agent.pillar_name,
            "status": "active",
            "peer_agents_registered": len(agent.peer_agents)
        }
    
    return {
        "status": "active",
        "total_agents": len(orchestrator.agents),
        "collaboration_protocol": "A2A (Agent-to-Agent)",
        "ai_framework": "Microsoft Semantic Kernel",
        "agents": agent_status,
        "collaboration_sessions": len(orchestrator.collaboration_sessions)
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize the multi-agent system on startup"""
    initialize_orchestrator()

@app.on_event("shutdown")
async def shutdown_db_client():
    if orchestrator:
        await orchestrator.cleanup()
    client.close()
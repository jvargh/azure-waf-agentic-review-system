#!/usr/bin/env python3
"""
Test database update operations
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

# Load environment
ROOT_DIR = Path(__file__).parent / "backend"
load_dotenv(ROOT_DIR / '.env')

async def test_db_operations():
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Test assessment ID from our debug test
    assessment_id = "4711a7b2-78e2-4e71-80dd-969ceefb1f89"
    
    print(f"Testing database operations for assessment: {assessment_id}")
    
    # Check if assessment exists
    assessment = await db.assessments.find_one({"id": assessment_id})
    if assessment:
        print(f"Assessment found: {assessment['name']}")
        print(f"Current keys: {list(assessment.keys())}")
        
        # Try to update with reactive data
        test_csv = "test,data\n1,2"
        test_results = {"test": "data", "analysis": {"total": 1}}
        
        print("\nTesting CSV content update...")
        result1 = await db.assessments.update_one(
            {"id": assessment_id},
            {"$set": {"reactive_cases_csv": test_csv}}
        )
        print(f"CSV update result: matched={result1.matched_count}, modified={result1.modified_count}")
        
        print("\nTesting reactive results update...")
        result2 = await db.assessments.update_one(
            {"id": assessment_id},
            {"$set": {"reactive_analysis_results": test_results}}
        )
        print(f"Results update result: matched={result2.matched_count}, modified={result2.modified_count}")
        
        # Check if updates worked
        updated_assessment = await db.assessments.find_one({"id": assessment_id})
        print(f"\nAfter updates:")
        print(f"Has reactive_cases_csv: {'reactive_cases_csv' in updated_assessment}")
        print(f"Has reactive_analysis_results: {'reactive_analysis_results' in updated_assessment}")
        
        if 'reactive_cases_csv' in updated_assessment:
            print(f"CSV content: {updated_assessment['reactive_cases_csv']}")
        if 'reactive_analysis_results' in updated_assessment:
            print(f"Results: {updated_assessment['reactive_analysis_results']}")
    else:
        print("Assessment not found!")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(test_db_operations())
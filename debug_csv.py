#!/usr/bin/env python3
"""
Debug CSV processing issue
"""

import requests
import json

BASE_URL = "https://arch-analyzer-2.preview.emergentagent.com/api"

# Create a simple CSV content
csv_content = """Case ID,Title,Priority,Category,Status
CASE-001,Database timeout,High,Reliability,Resolved
CASE-002,Auth failure,Critical,Security,Open"""

# Create assessment
assessment_data = {
    "name": "Debug CSV Test",
    "description": "Testing CSV processing debug"
}

response = requests.post(f"{BASE_URL}/assessments", json=assessment_data)
if response.status_code == 200:
    assessment_id = response.json()["id"]
    print(f"Created assessment: {assessment_id}")
    
    # Upload CSV file
    with open("/tmp/debug.csv", "w") as f:
        f.write(csv_content)
    
    with open("/tmp/debug.csv", "rb") as f:
        files = {"file": ("debug.csv", f, "text/csv")}
        response = requests.post(f"{BASE_URL}/assessments/{assessment_id}/documents", files=files)
        
        print(f"Upload response status: {response.status_code}")
        print(f"Upload response: {json.dumps(response.json(), indent=2)}")
        
        # Check assessment data
        response = requests.get(f"{BASE_URL}/assessments/{assessment_id}")
        data = response.json()
        
        print(f"\nAssessment keys: {list(data.keys())}")
        print(f"Has reactive_cases_csv: {'reactive_cases_csv' in data}")
        print(f"Has reactive_analysis_results: {'reactive_analysis_results' in data}")
        
        if 'reactive_cases_csv' in data:
            print(f"Reactive CSV length: {len(data['reactive_cases_csv'])}")
        if 'reactive_analysis_results' in data:
            print(f"Reactive results: {data['reactive_analysis_results']}")
else:
    print(f"Failed to create assessment: {response.status_code} - {response.text}")
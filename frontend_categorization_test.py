#!/usr/bin/env python3
"""
Frontend Categorization Test
Tests the actual frontend behavior by simulating the exact scenario described by the user.
"""

import requests
import json
import time
import base64
import os
from datetime import datetime
import tempfile

# Configuration
BASE_URL = "https://arch-analyzer-2.preview.emergentagent.com/api"
TIMEOUT = 30

class FrontendCategorizationTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.test_assessment_id = None
        self.test_results = []
        
    def log_test(self, test_name, success, message, details=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details:
            print(f"   Details: {json.dumps(details, indent=2)}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def create_test_files(self):
        """Create test files exactly as a user would upload them"""
        test_files = {}
        
        # Create a text file (architecture document)
        txt_content = """
Azure E-commerce Platform Architecture
=====================================

OVERVIEW:
This document describes our multi-tier e-commerce platform built on Microsoft Azure.

ARCHITECTURE COMPONENTS:

Frontend Tier:
- React.js application hosted on Azure Static Web Apps
- Azure CDN for global content delivery
- Custom domain with SSL certificate

Application Tier:
- Azure App Service (Premium P2V2) for API backend
- Azure Application Gateway for load balancing
- Azure API Management for API governance

Data Tier:
- Azure SQL Database (Business Critical, Gen5 8 vCores)
- Azure Cache for Redis (Premium P1) for session storage
- Azure Blob Storage for product images and documents

Security:
- Azure Active Directory B2C for customer authentication
- Azure Key Vault for secrets and certificate management
- Network Security Groups for network isolation
- Azure Firewall for outbound traffic control

Monitoring:
- Azure Monitor for infrastructure monitoring
- Application Insights for application performance monitoring
- Azure Log Analytics for centralized logging

DEPLOYMENT:
- Multi-region deployment (Primary: East US, Secondary: West Europe)
- Azure Traffic Manager for DNS-based load balancing
- Automated CI/CD pipeline using Azure DevOps

COMPLIANCE:
- PCI DSS compliance for payment processing
- GDPR compliance for EU customers
- SOC 2 Type II certification
        """
        
        # Create a CSV file (support cases)
        csv_content = """Case ID,Title,Category,Priority,Status,Azure Service,Issue Description,Resolution
CASE-001,High Memory Usage,Performance,High,Resolved,Azure App Service,App Service instances consuming 95% memory during peak hours,Scaled out to 4 instances and optimized memory usage
CASE-002,SQL Timeout Errors,Reliability,Critical,Open,Azure SQL Database,Database queries timing out during high traffic periods,Investigating query performance and considering read replicas
CASE-003,Storage Cost Spike,Cost Optimization,Medium,Resolved,Azure Blob Storage,Monthly storage costs increased by 300% unexpectedly,Implemented lifecycle management policies to move old data to cool tier
CASE-004,Login Failures,Security,High,Open,Azure AD B2C,Users experiencing intermittent login failures,Reviewing conditional access policies and authentication flows
CASE-005,Cache Performance,Performance,Medium,Open,Azure Cache for Redis,High cache miss rate affecting application performance,Analyzing cache key patterns and expiration policies
CASE-006,CDN Issues,Performance,Low,Resolved,Azure CDN,Slow content delivery in Asia-Pacific region,Added additional CDN endpoints in Singapore and Sydney
CASE-007,Backup Failures,Reliability,High,Open,Azure SQL Database,Automated database backups failing intermittently,Investigating backup storage and retention policies
CASE-008,SSL Certificate,Security,Medium,Resolved,Azure App Service,SSL certificate expired causing HTTPS errors,Renewed certificate and set up auto-renewal
CASE-009,Monitoring Gaps,Operational Excellence,Medium,Open,Azure Monitor,Missing critical alerts for database performance,Configuring comprehensive alerting rules
CASE-010,Data Encryption,Security,Critical,Open,Azure SQL Database,Sensitive customer data not encrypted at rest,Implementing Transparent Data Encryption (TDE)
        """
        
        # Create test files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(txt_content)
            test_files['txt'] = {
                'path': f.name,
                'filename': 'azure_ecommerce_architecture.txt',
                'content_type': 'text/plain',
                'content': txt_content
            }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            test_files['csv'] = {
                'path': f.name,
                'filename': 'support_cases_analysis.csv',
                'content_type': 'text/csv',
                'content': csv_content
            }
        
        # Create a simple PNG image (architecture diagram)
        # This is a 1x1 pixel transparent PNG
        png_data = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==')
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            f.write(png_data)
            test_files['png'] = {
                'path': f.name,
                'filename': 'azure_architecture_diagram.png',
                'content_type': 'image/png',
                'content': png_data
            }
        
        return test_files
    
    def cleanup_test_files(self, test_files):
        """Clean up temporary test files"""
        for file_info in test_files.values():
            try:
                os.unlink(file_info['path'])
            except:
                pass
    
    def test_user_scenario_simulation(self):
        """Simulate the exact user scenario: create assessment, upload files, check categorization"""
        print("🎭 SIMULATING USER SCENARIO")
        print("=" * 60)
        
        # Step 1: Create assessment
        print("\n📝 Step 1: Creating assessment...")
        assessment_data = {
            "name": "User Scenario Test - E-commerce Platform Review",
            "description": "Testing the exact scenario reported by the user where CSV files and images don't show up properly in Artifact Findings tab."
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/assessments",
                json=assessment_data,
                timeout=TIMEOUT
            )
            
            if response.status_code != 200:
                self.log_test("User Scenario - Create Assessment", False, f"HTTP {response.status_code}", response.text)
                return False
            
            self.test_assessment_id = response.json()["id"]
            print(f"   ✅ Assessment created: {self.test_assessment_id}")
            
        except Exception as e:
            self.log_test("User Scenario - Create Assessment", False, f"Error: {str(e)}")
            return False
        
        # Step 2: Upload different file types
        print("\n📁 Step 2: Uploading different file types...")
        test_files = self.create_test_files()
        uploaded_files = []
        
        try:
            for file_type, file_info in test_files.items():
                print(f"   Uploading {file_type.upper()}: {file_info['filename']}")
                
                with open(file_info['path'], 'rb') as f:
                    files = {"file": (file_info['filename'], f, file_info['content_type'])}
                    response = self.session.post(
                        f"{self.base_url}/assessments/{self.test_assessment_id}/documents",
                        files=files,
                        timeout=TIMEOUT
                    )
                
                if response.status_code == 200:
                    uploaded_files.append({
                        'type': file_type,
                        'filename': file_info['filename'],
                        'expected_content_type': file_info['content_type'],
                        'document_id': response.json().get('document_id')
                    })
                    print(f"      ✅ Uploaded successfully")
                else:
                    print(f"      ❌ Upload failed: {response.status_code}")
                    self.log_test("User Scenario - File Upload", False, f"Failed to upload {file_type}", response.text)
                    return False
            
        except Exception as e:
            self.log_test("User Scenario - File Upload", False, f"Upload error: {str(e)}")
            return False
        finally:
            self.cleanup_test_files(test_files)
        
        # Step 3: Check what the frontend would receive
        print("\n🔍 Step 3: Checking API response (what frontend receives)...")
        
        try:
            response = self.session.get(f"{self.base_url}/assessments/{self.test_assessment_id}", timeout=TIMEOUT)
            
            if response.status_code != 200:
                self.log_test("User Scenario - API Response", False, f"HTTP {response.status_code}", response.text)
                return False
            
            assessment_data = response.json()
            documents = assessment_data.get("documents", [])
            
            print(f"   📋 API returned {len(documents)} documents")
            
            # Simulate frontend categorization logic
            frontend_categorization = self.simulate_frontend_categorization(documents)
            
            # Step 4: Analyze the results
            print("\n📊 Step 4: Analyzing categorization results...")
            
            analysis_results = {
                "total_uploaded": len(uploaded_files),
                "total_received": len(documents),
                "frontend_categorization": frontend_categorization,
                "categorization_issues": [],
                "missing_files": [],
                "content_type_issues": []
            }
            
            # Check if all uploaded files are present
            received_filenames = [doc.get('filename', '') for doc in documents]
            for uploaded_file in uploaded_files:
                if uploaded_file['filename'] not in received_filenames:
                    analysis_results["missing_files"].append(uploaded_file['filename'])
            
            # Check content types
            for doc in documents:
                filename = doc.get('filename', '')
                content_type = doc.get('content_type', '')
                
                # Find the corresponding uploaded file
                uploaded_file = next((uf for uf in uploaded_files if uf['filename'] == filename), None)
                if uploaded_file and uploaded_file['expected_content_type'] != content_type:
                    analysis_results["content_type_issues"].append({
                        'filename': filename,
                        'expected': uploaded_file['expected_content_type'],
                        'actual': content_type
                    })
            
            # Check categorization issues
            expected_categories = {
                'azure_ecommerce_architecture.txt': 'text',
                'support_cases_analysis.csv': 'csv',
                'azure_architecture_diagram.png': 'image'
            }
            
            for filename, expected_category in expected_categories.items():
                actual_category = None
                
                if filename in [doc['filename'] for doc in frontend_categorization['textDocuments']]:
                    actual_category = 'text'
                elif filename in [doc['filename'] for doc in frontend_categorization['csvDocuments']]:
                    actual_category = 'csv'
                elif filename in [doc['filename'] for doc in frontend_categorization['imageDocuments']]:
                    actual_category = 'image'
                else:
                    actual_category = 'other'
                
                if actual_category != expected_category:
                    analysis_results["categorization_issues"].append({
                        'filename': filename,
                        'expected_category': expected_category,
                        'actual_category': actual_category
                    })
            
            # Determine if the user's issue is reproduced
            has_categorization_issues = (
                len(analysis_results["categorization_issues"]) > 0 or
                len(analysis_results["missing_files"]) > 0 or
                len(analysis_results["content_type_issues"]) > 0
            )
            
            if has_categorization_issues:
                self.log_test("User Scenario - Issue Reproduction", True, 
                            "Successfully reproduced the user's categorization issue", analysis_results)
            else:
                self.log_test("User Scenario - Issue Reproduction", False, 
                            "Could not reproduce the user's issue - categorization appears to work correctly", analysis_results)
            
            return analysis_results
            
        except Exception as e:
            self.log_test("User Scenario - Analysis", False, f"Analysis error: {str(e)}")
            return False
    
    def simulate_frontend_categorization(self, documents):
        """Simulate the exact frontend categorization logic from App.js"""
        print("   🧠 Simulating frontend categorization logic...")
        
        # This is the exact logic from the ArtifactFindingsTab component
        textDocuments = []
        imageDocuments = []
        csvDocuments = []
        otherDocuments = []
        
        for doc in documents:
            filename = doc.get('filename', '').lower()
            content_type = doc.get('content_type', '').lower()
            
            print(f"      📄 Processing: {doc.get('filename', 'Unknown')}")
            print(f"         Content-Type: {content_type}")
            print(f"         Filename: {filename}")
            
            # Text documents check
            is_text = (
                content_type == 'text/plain' or 
                'text' in content_type or
                filename.endswith('.txt') or 
                filename.endswith('.md') or
                filename.endswith('.doc') or
                filename.endswith('.docx') or
                (content_type == 'application/octet-stream' and (filename.endswith('.txt') or filename.endswith('.md')))
            )
            
            # Image documents check
            is_image = (
                content_type.startswith('image/') or
                filename.endswith('.png') or
                filename.endswith('.jpg') or
                filename.endswith('.jpeg') or
                filename.endswith('.gif') or
                filename.endswith('.bmp') or
                filename.endswith('.svg') or
                (content_type == 'application/octet-stream' and 
                 (filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg')))
            )
            
            # CSV documents check
            is_csv = (
                content_type == 'text/csv' or 
                'csv' in content_type or
                filename.endswith('.csv') or
                (content_type == 'application/octet-stream' and filename.endswith('.csv'))
            )
            
            # Categorize
            if is_text and not is_csv:  # Text files but not CSV
                textDocuments.append(doc)
                print(f"         ➡️ Categorized as: TEXT")
            elif is_image:
                imageDocuments.append(doc)
                print(f"         ➡️ Categorized as: IMAGE")
            elif is_csv:
                csvDocuments.append(doc)
                print(f"         ➡️ Categorized as: CSV")
            else:
                otherDocuments.append(doc)
                print(f"         ➡️ Categorized as: OTHER")
        
        categorization_result = {
            'textDocuments': textDocuments,
            'imageDocuments': imageDocuments,
            'csvDocuments': csvDocuments,
            'otherDocuments': otherDocuments,
            'summary': {
                'total': len(documents),
                'text': len(textDocuments),
                'images': len(imageDocuments),
                'csv': len(csvDocuments),
                'other': len(otherDocuments)
            }
        }
        
        print(f"   📊 Categorization Summary:")
        print(f"      Total: {categorization_result['summary']['total']}")
        print(f"      Text: {categorization_result['summary']['text']}")
        print(f"      Images: {categorization_result['summary']['images']}")
        print(f"      CSV: {categorization_result['summary']['csv']}")
        print(f"      Other: {categorization_result['summary']['other']}")
        
        return categorization_result
    
    def run_frontend_test(self):
        """Run the frontend categorization test"""
        print("🎯 FRONTEND CATEGORIZATION INVESTIGATION")
        print("Testing the exact user scenario to identify categorization issues")
        print("=" * 80)
        
        results = self.test_user_scenario_simulation()
        
        # Calculate test results
        passed_tests = sum(1 for result in self.test_results if result["success"])
        total_tests = len(self.test_results)
        
        print("\n" + "=" * 80)
        print(f"📊 FRONTEND TEST SUMMARY: {passed_tests}/{total_tests} tests passed")
        
        if results:
            print("\n🔍 INVESTIGATION FINDINGS:")
            if results.get("categorization_issues"):
                print("❌ CATEGORIZATION ISSUES FOUND:")
                for issue in results["categorization_issues"]:
                    print(f"   • {issue['filename']}: Expected {issue['expected_category']}, got {issue['actual_category']}")
            
            if results.get("content_type_issues"):
                print("❌ CONTENT TYPE ISSUES FOUND:")
                for issue in results["content_type_issues"]:
                    print(f"   • {issue['filename']}: Expected {issue['expected']}, got {issue['actual']}")
            
            if results.get("missing_files"):
                print("❌ MISSING FILES:")
                for filename in results["missing_files"]:
                    print(f"   • {filename}")
            
            if not results.get("categorization_issues") and not results.get("content_type_issues") and not results.get("missing_files"):
                print("✅ NO ISSUES FOUND - Categorization appears to work correctly")
        
        return passed_tests, total_tests, self.test_results, results

def main():
    """Main test execution"""
    tester = FrontendCategorizationTester()
    passed, total, test_results, analysis_results = tester.run_frontend_test()
    
    # Save detailed results
    with open("/app/frontend_categorization_test_results.json", "w") as f:
        json.dump({
            "summary": {
                "passed": passed,
                "total": total,
                "success_rate": f"{(passed/total)*100:.1f}%"
            },
            "test_results": test_results,
            "analysis_results": analysis_results,
            "test_run_timestamp": datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: /app/frontend_categorization_test_results.json")
    
    return analysis_results

if __name__ == "__main__":
    results = main()
    exit(0)
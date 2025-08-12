#!/usr/bin/env python3
"""
Simple API Test Script for QESTIT API
Run this script to test the API endpoints
"""

import requests
import json
import os
from datetime import datetime

# API Configuration
BASE_URL = "http://localhost:8000"
API_ENDPOINTS = {
    "info": "/",
    "health": "/health",
    "outputs": "/api/outputs",
    "file_list": "/api/file-list",
    "full_workflow": "/api/full-workflow"
}

def test_endpoint(endpoint, method="GET", data=None, files=None):
    """Test a specific API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n{'='*60}")
    print(f"Testing: {method} {url}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, data=data, files=files)
        else:
            print(f"Unsupported method: {method}")
            return None
            
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                json_response = response.json()
                print(f"Response Body (JSON):")
                print(json.dumps(json_response, indent=2))
                return json_response
            except json.JSONDecodeError:
                print(f"Response Body (Text): {response.text[:500]}...")
                return response.text
        else:
            print(f"Error Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def test_basic_endpoints():
    """Test basic API endpoints"""
    print("Testing Basic API Endpoints...")
    
    # Test API info
    test_endpoint(API_ENDPOINTS["info"])
    
    # Test health check
    test_endpoint(API_ENDPOINTS["health"])
    
    # Test outputs listing
    test_endpoint(API_ENDPOINTS["outputs"])
    
    # Test file listing by type
    test_endpoint(f"{API_ENDPOINTS['file_list']}?file_type=md")
    test_endpoint(f"{API_ENDPOINTS['file_list']}?file_type=xlsx")
    test_endpoint(f"{API_ENDPOINTS['file_list']}?file_type=pdf")

def test_file_processing():
    """Test file processing workflow"""
    print("\nTesting File Processing Workflow...")
    
    # Check if we have a test file
    test_file_path = "test_document.txt"
    
    if not os.path.exists(test_file_path):
        # Create a simple test document
        test_content = """
        Banking System Requirements Document
        
        The system should allow customers to:
        1. View account balance
        2. Transfer funds between accounts
        3. Make payments to other accounts
        4. View transaction history
        
        Security Requirements:
        - Multi-factor authentication
        - Encrypted data transmission
        - Session timeout after 30 minutes
        
        Performance Requirements:
        - Response time < 2 seconds
        - Support 1000+ concurrent users
        - 99.9% uptime
        """
        
        with open(test_file_path, "w") as f:
            f.write(test_content)
        print(f"Created test document: {test_file_path}")
    
    # Test full workflow
    with open(test_file_path, "rb") as f:
        files = {"file": ("test_document.txt", f, "text/plain")}
        data = {
            "feature_prefix": "TC",
            "iteration_count": "50",  # Reduced for testing
            "user_story": "As a customer, I want to transfer funds between my accounts",
            "feature_title": "Fund Transfer Feature"
        }
        
        response = test_endpoint(API_ENDPOINTS["full_workflow"], "POST", data, files)
        
        if response and isinstance(response, dict):
            # Extract generated filenames for download testing
            workflow_steps = response.get("workflow_steps", {})
            
            if "step_4_test_cases" in workflow_steps:
                test_files = workflow_steps["step_4_test_cases"].get("files", {})
                
                # Test file downloads
                for file_type, file_path in test_files.items():
                    if file_path:
                        filename = os.path.basename(file_path)
                        print(f"\nTesting download for {file_type}: {filename}")
                        download_url = f"/api/download/{filename}"
                        test_endpoint(download_url)

def test_file_downloads():
    """Test file download functionality"""
    print("\nTesting File Downloads...")
    
    # First get the list of available files
    response = test_endpoint(API_ENDPOINTS["outputs"])
    
    if response and isinstance(response, dict):
        files = response.get("files", [])
        
        if files:
            print(f"Found {len(files)} files for download testing")
            
            # Test download of first few files
            for file_info in files[:3]:  # Test first 3 files
                filename = file_info.get("filename")
                if filename:
                    print(f"\nTesting download: {filename}")
                    download_url = f"/api/download/{filename}"
                    test_endpoint(download_url)
        else:
            print("No files found for download testing")

def main():
    """Main test function"""
    print("QESTIT API Test Script")
    print(f"Testing API at: {BASE_URL}")
    print(f"Timestamp: {datetime.now()}")
    
    try:
        # Test basic endpoints
        test_basic_endpoints()
        
        # Test file processing (optional - can be commented out for faster testing)
        # test_file_processing()
        
        # Test file downloads
        test_file_downloads()
        
        print("\n" + "="*60)
        print("API Testing Complete!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\nTesting interrupted by user")
    except Exception as e:
        print(f"\nTesting failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

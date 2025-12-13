#!/usr/bin/env python3
"""
CampusOps AI - Comprehensive API Endpoint Tester
=================================================

This script demonstrates and tests all available endpoints for both
Admin and Student users of the CampusOps AI RAG system.

Usage:
    python test_endpoints.py [--base-url URL]
    
Default base URL: http://localhost:8000
"""

import requests
import argparse
from typing import Optional
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_BASE_URL = "http://localhost:8000"


class CampusOpsClient:
    """Client for interacting with CampusOps AI API."""
    
    def __init__(self, base_url: str = DEFAULT_BASE_URL):
        self.base_url = base_url.rstrip("/")
        
    def _print_response(self, response: requests.Response, title: str):
        """Pretty print API response."""
        print(f"\n{'─'*60}")
        print(f"📍 {title}")
        print(f"{'─'*60}")
        print(f"Status: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except:
            print(f"Response: {response.text[:500]}")
        print()


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH ENDPOINTS (Public)
# ═══════════════════════════════════════════════════════════════════════════════

class HealthEndpoints:
    """
    Health check endpoints - accessible by anyone.
    
    These endpoints check if the API is running and return system stats.
    """
    
    def __init__(self, client: CampusOpsClient):
        self.client = client
        
    def health_check(self) -> dict:
        """
        GET /
        
        Check if the API is healthy and get the number of chunks in the database.
        
        Returns:
            {
                "status": "ok",
                "chunks_in_db": <int>
            }
        """
        response = requests.get(f"{self.client.base_url}/")
        self.client._print_response(response, "Health Check")
        return response.json()


# ═══════════════════════════════════════════════════════════════════════════════
# STUDENT ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

class StudentEndpoints:
    """
    Student endpoints for querying campus policies.
    
    Students can ask questions about:
    - Attendance policies
    - Examination rules
    - Eligibility and promotion rules
    - Placement policies
    - Academic calendar
    - Administrative guidelines
    - Campus events and activities
    """
    
    def __init__(self, client: CampusOpsClient):
        self.client = client
    
    def ask_question(self, question: str) -> dict:
        """
        POST /query/
        
        Ask a question about campus policies. The RAG system will retrieve
        relevant chunks from the knowledge base and generate an AI answer.
        
        Args:
            question: The question to ask (e.g., "What is the minimum attendance required?")
            
        Returns:
            {
                "answer": <str>,      # AI-generated answer
                "sources": [<str>]    # Source chunks used for the answer
            }
        """
        payload = {"query": question}
        response = requests.post(f"{self.client.base_url}/query/", json=payload)
        self.client._print_response(response, f"Student Query: {question}")
        return response.json()


# ═══════════════════════════════════════════════════════════════════════════════
# ADMIN ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

class AdminEndpoints:
    """
    Admin endpoints for managing the knowledge base.
    
    Admins can:
    - Upload/download/delete policy files
    - View all uploaded files
    - Ingest documents directly
    - View knowledge base statistics
    """
    
    def __init__(self, client: CampusOpsClient):
        self.client = client
    
    # ─────────────────────────────────────────────────────────────
    # File Management
    # ─────────────────────────────────────────────────────────────
    
    def list_files(self) -> dict:
        """
        GET /admin/files
        
        List all uploaded files in the knowledge base.
        
        Returns:
            {
                "files": [
                    {
                        "filename": <str>,
                        "size_bytes": <int>,
                        "uploaded_at": <str>
                    },
                    ...
                ],
                "total_count": <int>
            }
        """
        response = requests.get(f"{self.client.base_url}/admin/files")
        self.client._print_response(response, "List All Files")
        return response.json()
    
    def upload_file(self, filepath: str) -> dict:
        """
        POST /admin/files
        
        Upload a .txt file. The file will be saved and automatically indexed.
        Chunks are separated by blank lines in the file.
        
        Args:
            filepath: Path to the .txt file to upload
            
        Returns:
            {
                "message": <str>,
                "filename": <str>,
                "size_bytes": <int>,
                "chunks_added": <int>
            }
        """
        with open(filepath, "rb") as f:
            files = {"file": (Path(filepath).name, f, "text/plain")}
            response = requests.post(f"{self.client.base_url}/admin/files", files=files)
        self.client._print_response(response, f"Upload File: {filepath}")
        return response.json()
    
    def download_file(self, filename: str) -> str:
        """
        GET /admin/files/{filename}
        
        Download/view a specific file's content.
        
        Args:
            filename: Name of the file to download
            
        Returns:
            File content as string
        """
        response = requests.get(f"{self.client.base_url}/admin/files/{filename}")
        self.client._print_response(response, f"Download File: {filename}")
        return response.text
    
    def delete_file(self, filename: str) -> dict:
        """
        DELETE /admin/files/{filename}
        
        Delete a file and all its indexed chunks from the knowledge base.
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            {
                "message": <str>,
                "filename": <str>,
                "chunks_deleted": <int>
            }
        """
        response = requests.delete(f"{self.client.base_url}/admin/files/{filename}")
        self.client._print_response(response, f"Delete File: {filename}")
        return response.json()
    
    # ─────────────────────────────────────────────────────────────
    # Direct Ingestion
    # ─────────────────────────────────────────────────────────────
    
    def ingest_documents(self, documents: list[str]) -> dict:
        """
        POST /admin/ingest
        
        Directly ingest document chunks into the knowledge base.
        These chunks won't be associated with a file.
        
        Args:
            documents: List of document chunks to ingest
            
        Returns:
            {
                "message": <str>,
                "chunks_added": <int>
            }
        """
        payload = {"documents": documents}
        response = requests.post(f"{self.client.base_url}/admin/ingest", json=payload)
        self.client._print_response(response, "Ingest Documents")
        return response.json()
    
    # ─────────────────────────────────────────────────────────────
    # Statistics
    # ─────────────────────────────────────────────────────────────
    
    def get_stats(self) -> dict:
        """
        GET /admin/stats
        
        Get knowledge base statistics.
        
        Returns:
            {
                "total_chunks": <int>,
                "total_files": <int>
            }
        """
        response = requests.get(f"{self.client.base_url}/admin/stats")
        self.client._print_response(response, "Knowledge Base Stats")
        return response.json()


# ═══════════════════════════════════════════════════════════════════════════════
# API ENDPOINTS SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

ENDPOINTS_SUMMARY = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         CampusOps AI - API Endpoints                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  🏥 HEALTH (Public)                                                          ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  GET  /                    Health check + DB stats                           ║
║                                                                              ║
║  🎓 STUDENT ENDPOINTS                                                        ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  POST /query/              Ask a question about campus policies              ║
║                                                                              ║
║  🔐 ADMIN ENDPOINTS                                                          ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  GET    /admin/files                List all uploaded files                  ║
║  POST   /admin/files                Upload a new .txt file                   ║
║  GET    /admin/files/{filename}     Download/view a file                     ║
║  DELETE /admin/files/{filename}     Delete a file + its chunks               ║
║  POST   /admin/ingest               Ingest documents directly                ║
║  GET    /admin/stats                Get knowledge base statistics            ║
║                                                                              ║
║  📚 DOCUMENTATION                                                            ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║  GET  /docs                Swagger UI (interactive API docs)                 ║
║  GET  /redoc               ReDoc (alternative API docs)                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


# ═══════════════════════════════════════════════════════════════════════════════
# TEST RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_all_tests(base_url: str = DEFAULT_BASE_URL):
    """Run comprehensive tests on all endpoints."""
    
    print(ENDPOINTS_SUMMARY)
    print("\n" + "="*80)
    print("🚀 RUNNING COMPREHENSIVE ENDPOINT TESTS")
    print("="*80)
    
    client = CampusOpsClient(base_url)
    health = HealthEndpoints(client)
    student = StudentEndpoints(client)
    admin = AdminEndpoints(client)
    
    # ─────────────────────────────────────────────────────────────
    # Test 1: Health Check
    # ─────────────────────────────────────────────────────────────
    print("\n" + "═"*80)
    print("📋 TEST 1: Health Check")
    print("═"*80)
    
    try:
        health.health_check()
        print("✅ Health check passed!")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # ─────────────────────────────────────────────────────────────
    # Test 2: Admin - Get Stats
    # ─────────────────────────────────────────────────────────────
    print("\n" + "═"*80)
    print("📋 TEST 2: Admin - Get Knowledge Base Stats")
    print("═"*80)
    
    try:
        admin.get_stats()
        print("✅ Stats retrieved!")
    except Exception as e:
        print(f"❌ Stats retrieval failed: {e}")
    
    # ─────────────────────────────────────────────────────────────
    # Test 3: Admin - List Files
    # ─────────────────────────────────────────────────────────────
    print("\n" + "═"*80)
    print("📋 TEST 3: Admin - List All Files")
    print("═"*80)
    
    try:
        admin.list_files()
        print("✅ Files listed!")
    except Exception as e:
        print(f"❌ File listing failed: {e}")
    
    # ─────────────────────────────────────────────────────────────
    # Test 4: Student Queries
    # ─────────────────────────────────────────────────────────────
    print("\n" + "═"*80)
    print("📋 TEST 4: Student Queries (Testing RAG)")
    print("═"*80)
    
    sample_questions = [
        "What is the minimum attendance required for BTech students?",
        "What are the examination rules?",
        "Tell me about the placement policy",
        "When does the academic year start?",
        "What are the campus event guidelines?",
    ]
    
    for q in sample_questions:
        try:
            student.ask_question(q)
            print(f"✅ Query successful: {q[:50]}...")
        except Exception as e:
            print(f"❌ Query failed: {e}")
    
    # ─────────────────────────────────────────────────────────────
    # Test 5: Admin - Direct Document Ingestion
    # ─────────────────────────────────────────────────────────────
    print("\n" + "═"*80)
    print("📋 TEST 5: Admin - Direct Document Ingestion")
    print("═"*80)
    
    test_docs = [
        "Test Policy: Students must maintain a GPA of 2.0 to remain in good standing.",
        "Test Rule: Late submissions will incur a 10% penalty per day."
    ]
    
    try:
        admin.ingest_documents(test_docs)
        print("✅ Documents ingested!")
    except Exception as e:
        print(f"❌ Document ingestion failed: {e}")
    
    # ─────────────────────────────────────────────────────────────
    # Summary
    # ─────────────────────────────────────────────────────────────
    print("\n" + "═"*80)
    print("📊 TEST SUMMARY")
    print("═"*80)
    print("""
All tests completed. Check the output above for results.

Available data files in the system:
  📄 Academic_Calendar_2024.txt
  📄 Administrative_Circular_Guidelines.txt
  📄 BTech_Attendance_Policy.txt
  📄 BTech_Eligibility_and_Promotion_Rules.txt
  📄 BTech_Examination_Rules.txt
  📄 BTech_Placement_Policy.txt
  📄 Campus_Events_and_Activities_Policy.txt
""")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE USAGE
# ═══════════════════════════════════════════════════════════════════════════════

def show_examples():
    """Show example code for using the API."""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         EXAMPLE USAGE                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

# ─────────────────────────────────────────────────────────────
# 1. Using the Client Classes
# ─────────────────────────────────────────────────────────────

from test_endpoints import CampusOpsClient, StudentEndpoints, AdminEndpoints

client = CampusOpsClient("http://localhost:8000")
student = StudentEndpoints(client)
admin = AdminEndpoints(client)

# Student: Ask a question
result = student.ask_question("What is the attendance policy?")
print(result["answer"])

# Admin: Upload a file
admin.upload_file("data/new_policy.txt")

# Admin: List all files
files = admin.list_files()
print(files["files"])

# Admin: Get stats
stats = admin.get_stats()
print(f"Total chunks: {stats['total_chunks']}")

# ─────────────────────────────────────────────────────────────
# 2. Using cURL Commands
# ─────────────────────────────────────────────────────────────

# Health Check
curl http://localhost:8000/

# Student Query
curl -X POST http://localhost:8000/query/ \\
     -H "Content-Type: application/json" \\
     -d '{"query": "What is the attendance policy?"}'

# Admin: List Files
curl http://localhost:8000/admin/files

# Admin: Upload File
curl -X POST http://localhost:8000/admin/files \\
     -F "file=@data/new_policy.txt"

# Admin: Download File
curl http://localhost:8000/admin/files/BTech_Attendance_Policy.txt

# Admin: Delete File
curl -X DELETE http://localhost:8000/admin/files/old_policy.txt

# Admin: Ingest Documents
curl -X POST http://localhost:8000/admin/ingest \\
     -H "Content-Type: application/json" \\
     -d '{"documents": ["Policy chunk 1", "Policy chunk 2"]}'

# Admin: Get Stats
curl http://localhost:8000/admin/stats

# ─────────────────────────────────────────────────────────────
# 3. Using Python requests Directly
# ─────────────────────────────────────────────────────────────

import requests

BASE_URL = "http://localhost:8000"

# Student Query
response = requests.post(f"{BASE_URL}/query/", json={
    "query": "What are the eligibility criteria for promotion?"
})
data = response.json()
print(f"Answer: {data['answer']}")
print(f"Sources: {data['sources']}")

# Admin: Upload File
with open("data/new_policy.txt", "rb") as f:
    response = requests.post(f"{BASE_URL}/admin/files", files={"file": f})
print(response.json())
""")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CampusOps AI - Comprehensive API Endpoint Tester",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=ENDPOINTS_SUMMARY
    )
    parser.add_argument(
        "--base-url", 
        default=DEFAULT_BASE_URL,
        help=f"Base URL for the API (default: {DEFAULT_BASE_URL})"
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Show example usage code"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show endpoint summary only"
    )
    
    args = parser.parse_args()
    
    if args.summary:
        print(ENDPOINTS_SUMMARY)
    elif args.examples:
        show_examples()
    else:
        run_all_tests(args.base_url)

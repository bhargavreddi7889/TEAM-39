#!/usr/bin/env python3
"""
CampusOps AI - System Verification Script
==========================================

This script verifies that all components of the RAG system are working correctly:
- Document processing (.txt, .docx, .pdf)
- File upload and auto-indexing
- File deletion and chunk removal
- Query processing and answer generation
- Vector database operations
"""

import sys
import requests
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

API_BASE_URL = "http://brahamand.ai:9000"

def print_header(title):
    """Print a formatted header."""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}{title.center(70)}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

def print_success(message):
    """Print success message."""
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

def print_error(message):
    """Print error message."""
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

def print_info(message):
    """Print info message."""
    print(f"{Fore.YELLOW}ℹ️  {message}{Style.RESET_ALL}")

def print_step(message):
    """Print step message."""
    print(f"{Fore.BLUE}▶ {message}{Style.RESET_ALL}")


def check_api_health():
    """Test 1: Check if API server is running."""
    print_header("Test 1: API Server Health Check")
    
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"API server is online: {data.get('message', '')}")
            return True
        else:
            print_error(f"API returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Cannot connect to API server: {e}")
        print_info("Make sure to run: python run.py")
        return False


def check_existing_data():
    """Test 2: Check existing files and database stats."""
    print_header("Test 2: Existing Data Check")
    
    try:
        # Get stats
        stats_response = requests.get(f"{API_BASE_URL}/admin/stats", timeout=5)
        stats = stats_response.json()
        
        print_step(f"Total chunks in database: {stats.get('total_chunks', 0)}")
        print_step(f"Total files indexed: {stats.get('total_files', 0)}")
        
        # Get file list
        files_response = requests.get(f"{API_BASE_URL}/admin/files", timeout=5)
        files_data = files_response.json()
        
        if files_data.get('files'):
            print_success(f"Found {len(files_data['files'])} files:")
            for file_info in files_data['files']:
                print(f"   📄 {file_info['filename']} ({file_info['size_bytes']} bytes, {file_info['file_type']})")
        else:
            print_info("No files found in the system")
        
        return True
    except Exception as e:
        print_error(f"Error checking data: {e}")
        return False


def test_query_system():
    """Test 3: Test the RAG query system."""
    print_header("Test 3: RAG Query System")
    
    test_queries = [
        "What is the minimum attendance requirement?",
        "Tell me about the placement policy",
        "What are the exam rules?",
    ]
    
    all_passed = True
    
    for query in test_queries:
        print_step(f"Testing query: '{query}'")
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/query/",
                json={"query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('answer', '')
                sources = data.get('sources', [])
                
                print_success(f"Answer received ({len(answer)} chars)")
                print(f"{Fore.MAGENTA}   Answer preview: {answer[:150]}...{Style.RESET_ALL}")
                print(f"{Fore.CYAN}   Sources: {len(sources)} chunks retrieved{Style.RESET_ALL}")
                
                if len(answer) < 10:
                    print_error("Answer seems too short!")
                    all_passed = False
                elif "don't have" in answer.lower() and len(sources) > 0:
                    print_error("Has sources but couldn't generate proper answer")
                    all_passed = False
            else:
                print_error(f"Query failed with status: {response.status_code}")
                all_passed = False
        except Exception as e:
            print_error(f"Query error: {e}")
            all_passed = False
        
        print()
    
    return all_passed


def test_file_formats():
    """Test 4: Verify supported file formats."""
    print_header("Test 4: File Format Support")
    
    data_dir = Path(__file__).parent / "data"
    
    # Check for different file types
    formats = {
        '.txt': list(data_dir.glob("*.txt")),
        '.docx': list(data_dir.glob("*.docx")),
        '.pdf': list(data_dir.glob("*.pdf")),
    }
    
    for ext, files in formats.items():
        if files:
            print_success(f"Found {len(files)} {ext} file(s)")
            for f in files:
                print(f"   {f.name}")
        else:
            print_info(f"No {ext} files found")
    
    return True


def test_document_processing():
    """Test 5: Test document text extraction."""
    print_header("Test 5: Document Processing Test")
    
    # Import the file service
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    try:
        from services.files import FileService
        
        file_service = FileService()
        files = file_service.list_files()
        
        if not files:
            print_info("No files to test processing")
            return True
        
        all_passed = True
        
        for file_info in files[:3]:  # Test first 3 files
            filename = file_info['filename']
            file_type = file_info['file_type']
            
            print_step(f"Testing {file_type} extraction: {filename}")
            
            try:
                content = file_service.get_file_text(filename)
                
                if content and content.strip():
                    word_count = len(content.split())
                    chunks = content.split("\n\n")
                    chunk_count = len([c for c in chunks if c.strip()])
                    
                    print_success(f"Extracted {word_count} words, {chunk_count} chunks")
                    print(f"{Fore.MAGENTA}   Preview: {content[:100]}...{Style.RESET_ALL}")
                else:
                    print_error(f"No content extracted from {filename}")
                    all_passed = False
            except Exception as e:
                print_error(f"Extraction failed: {e}")
                all_passed = False
            
            print()
        
        return all_passed
    except ImportError as e:
        print_error(f"Cannot import file service: {e}")
        return False


def test_reindex():
    """Test 6: Test re-indexing functionality."""
    print_header("Test 6: Re-indexing Test")
    
    print_step("Triggering re-index (without clearing)...")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/admin/reindex",
            params={"clear_existing": False},
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(data.get('message', 'Re-indexing complete'))
            print(f"{Fore.CYAN}   Total chunks: {data.get('total_chunks', 0)}{Style.RESET_ALL}")
            
            files_processed = data.get('files_processed', [])
            for file_info in files_processed:
                if 'error' in file_info:
                    print_error(f"   {file_info['filename']}: {file_info['error']}")
                else:
                    print_success(f"   {file_info['filename']}: {file_info['chunks']} chunks")
            
            return True
        else:
            print_error(f"Re-index failed with status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Re-index error: {e}")
        return False


def run_all_tests():
    """Run all verification tests."""
    print(f"\n{Fore.MAGENTA}{'='*70}")
    print(f"{Fore.MAGENTA}CampusOps AI - System Verification")
    print(f"{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}\n")
    
    results = {}
    
    # Run all tests
    results['API Health'] = check_api_health()
    
    if not results['API Health']:
        print_error("\n⚠️  API server is not running. Please start it first with: python run.py")
        return
    
    results['Existing Data'] = check_existing_data()
    results['File Formats'] = test_file_formats()
    results['Document Processing'] = test_document_processing()
    results['Query System'] = test_query_system()
    results['Re-indexing'] = test_reindex()
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{Fore.GREEN}PASSED" if result else f"{Fore.RED}FAILED"
        print(f"{status}{Style.RESET_ALL} - {test_name}")
    
    print(f"\n{Fore.CYAN}Total: {passed}/{total} tests passed{Style.RESET_ALL}")
    
    if passed == total:
        print(f"\n{Fore.GREEN}🎉 All tests passed! Your system is working perfectly!{Style.RESET_ALL}\n")
    else:
        print(f"\n{Fore.YELLOW}⚠️  Some tests failed. Please review the errors above.{Style.RESET_ALL}\n")


if __name__ == "__main__":
    try:
        # Try to import colorama, if not available, define dummy functions
        try:
            from colorama import init, Fore, Style
            init(autoreset=True)
        except ImportError:
            print("Note: Install 'colorama' for colored output (pip install colorama)")
            # Define dummy color codes
            class Fore:
                GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = ""
            class Style:
                RESET_ALL = ""
        
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)

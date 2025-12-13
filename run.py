#!/usr/bin/env python3
"""
CampusOps AI - Application Runner
==================================

Run the FastAPI backend and optionally the Streamlit UI.

Usage:
    python run.py              # Run API server only
    python run.py --ui         # Run API + Streamlit UI
    python run.py --ui-only    # Run Streamlit UI only
"""

import subprocess
import sys
import os

# Add the project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)


def run_api():
    """Run the FastAPI backend server."""
    print("🚀 Starting CampusOps AI API Server...")
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "src.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ], cwd=PROJECT_ROOT)


def run_ui():
    """Run the Streamlit UI."""
    print("🎨 Starting CampusOps AI Streamlit UI...")
    subprocess.run([
        sys.executable, "-m", "streamlit",
        "run", "src/app_ui.py",
        "--server.port", "8501"
    ], cwd=PROJECT_ROOT)


def run_both():
    """Run both API and UI in parallel."""
    import threading
    
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    print("\n⏳ Waiting for API to start...")
    import time
    time.sleep(3)
    
    run_ui()


if __name__ == "__main__":
    args = sys.argv[1:]
    
    if "--ui-only" in args:
        run_ui()
    elif "--ui" in args:
        run_both()
    else:
        run_api()

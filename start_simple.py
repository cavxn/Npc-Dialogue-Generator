#!/usr/bin/env python3
"""
Simple startup script for NPC Dialogue Generator
Uses the simple API and HTML frontend for guaranteed functionality
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import openai
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please run: pip install fastapi uvicorn openai python-dotenv")
        return False

def check_api_key():
    """Check if API key is configured"""
    env_path = Path("backend/.env")
    if not env_path.exists():
        print("❌ No .env file found")
        return False
    
    try:
        content = env_path.read_text()
        if "your_openai_api_key_here" in content or "OPENAI_API_KEY=" not in content:
            print("❌ OpenAI API key not configured")
            return False
        print("✅ API key is configured")
        return True
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def start_backend():
    """Start the simple backend API"""
    print("🚀 Starting Simple Backend API...")
    backend_path = Path(__file__).parent / "backend"
    os.chdir(backend_path)
    
    try:
        # Start the simple API server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "simple_api:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for startup
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Backend started on http://localhost:8000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def open_frontend():
    """Open the HTML frontend"""
    frontend_path = Path(__file__).parent / "simple_frontend.html"
    if frontend_path.exists():
        print("🌐 Opening frontend in browser...")
        webbrowser.open(f"file://{frontend_path.absolute()}")
        print("✅ Frontend opened at simple_frontend.html")
        return True
    else:
        print("❌ Frontend file not found")
        return False

def main():
    """Main startup function"""
    print("🎮 NPC Dialogue Generator - Simple Version")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Check API key
    if not check_api_key():
        print("\n📝 Please configure your OpenAI API key:")
        print("1. Get your API key from https://platform.openai.com/api-keys")
        print("2. Create backend/.env file with: OPENAI_API_KEY=your_key_here")
        return
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return
    
    # Wait a moment for backend to fully start
    time.sleep(2)
    
    # Open frontend
    if open_frontend():
        print("\n🎉 System is ready!")
        print("=" * 50)
        print("🌐 Frontend: simple_frontend.html (opened in browser)")
        print("🔧 Backend: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("\n✨ Features Available:")
        print("  • Character creation and dialogue generation")
        print("  • Character consistency and memory")
        print("  • Branching dialogue system")
        print("  • Translation (Spanish, French)")
        print("  • Real-time interactive chat")
        
        print("\n🛑 Press Ctrl+C to stop the backend")
        
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Shutting down backend...")
            backend_process.terminate()
            print("✅ Backend stopped")

if __name__ == "__main__":
    main()

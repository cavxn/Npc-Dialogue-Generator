#!/usr/bin/env python3
"""
Quick startup for NPC Dialogue Generator
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def main():
    print("🎮 Starting NPC Dialogue Generator...")
    
    # Check if .env exists
    env_path = Path("backend/.env")
    if not env_path.exists():
        print("❌ Please run setup_complete.py first")
        return
    
    # Check API key
    try:
        content = env_path.read_text()
        if "your_openai_api_key_here" in content:
            print("❌ Please configure your OpenAI API key in backend/.env")
            return
    except:
        print("❌ Error reading .env file")
        return
    
    # Start backend
    print("🚀 Starting backend...")
    backend_path = Path(__file__).parent / "backend"
    os.chdir(backend_path)
    
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "simple_api:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
        
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Backend started on http://localhost:8000")
            
            # Open frontend
            frontend_path = Path(__file__).parent / "simple_frontend.html"
            if frontend_path.exists():
                webbrowser.open(f"file://{frontend_path.absolute()}")
                print("✅ Frontend opened in browser")
            
            print("\n🎉 System is ready!")
            print("🌐 Frontend: simple_frontend.html")
            print("🔧 Backend: http://localhost:8000")
            print("📚 API Docs: http://localhost:8000/docs")
            print("\n🛑 Press Ctrl+C to stop")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n👋 Shutting down...")
                process.terminate()
        else:
            print("❌ Backend failed to start")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

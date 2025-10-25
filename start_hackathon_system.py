#!/usr/bin/env python3
"""
CodeZilla '25 Hackathon - NPC Dialogue Generator
Enhanced system with all required features for the hackathon
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_requirements():
    """Check if all required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import openai
        import websockets
        print("✅ All Python dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def start_backend():
    """Start the enhanced FastAPI backend"""
    print("🚀 Starting Enhanced NPC Dialogue API...")
    backend_path = Path(__file__).parent / "backend"
    os.chdir(backend_path)
    
    # Start the enhanced API server
    subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "enhanced_dialogue_api:app", 
        "--host", "0.0.0.0", 
        "--port", "8000", 
        "--reload"
    ])
    
    print("✅ Backend server started on http://localhost:8000")
    print("📚 API Documentation available at http://localhost:8000/docs")

def start_frontend():
    """Start the React frontend"""
    print("🎨 Starting React Frontend...")
    frontend_path = Path(__file__).parent / "frontend" / "npc-dialogue-ai"
    
    if not frontend_path.exists():
        print("❌ Frontend directory not found!")
        return False
    
    os.chdir(frontend_path)
    
    # Check if node_modules exists
    if not (frontend_path / "node_modules").exists():
        print("📦 Installing frontend dependencies...")
        subprocess.run(["npm", "install"], check=True)
    
    # Start the React development server
    subprocess.Popen(["npm", "start"])
    
    print("✅ Frontend started on http://localhost:3000")
    return True

def main():
    """Main startup function"""
    print("🎮 CodeZilla '25 - NPC Dialogue Generator")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Please run this script from the project root directory")
        return
    
    # Check requirements
    if not check_requirements():
        return
    
    print("\n🔧 Starting system components...")
    
    # Start backend
    start_backend()
    time.sleep(3)  # Give backend time to start
    
    # Start frontend
    if start_frontend():
        time.sleep(5)  # Give frontend time to start
        
        print("\n🎉 System is ready!")
        print("=" * 50)
        print("🌐 Frontend: http://localhost:3000")
        print("🔧 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("\n✨ Features Available:")
        print("  • Real-time dialogue with WebSocket support")
        print("  • Character consistency and memory")
        print("  • Branching dialogue system")
        print("  • Translation/localization (Spanish, French)")
        print("  • Interactive character selection")
        print("  • Personality-based dialogue generation")
        
        # Try to open the frontend in browser
        try:
            webbrowser.open("http://localhost:3000")
        except:
            print("\n💡 Open http://localhost:3000 in your browser to start!")
        
        print("\n🛑 Press Ctrl+C to stop all services")
        
        try:
            # Keep the script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Shutting down services...")
            print("✅ All services stopped")

if __name__ == "__main__":
    main()

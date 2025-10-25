#!/usr/bin/env python3
"""
Simple system runner for NPC Dialogue Generator
Starts both backend and frontend with proper error handling
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

class SystemRunner:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def start_backend(self):
        """Start the FastAPI backend"""
        print("🚀 Starting Backend API...")
        backend_path = Path(__file__).parent / "backend"
        os.chdir(backend_path)
        
        try:
            self.backend_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "enhanced_dialogue_api:app", 
                "--host", "0.0.0.0", 
                "--port", "8000"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait a moment for startup
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                print("✅ Backend started on http://localhost:8000")
                return True
            else:
                stdout, stderr = self.backend_process.communicate()
                print(f"❌ Backend failed to start:")
                print(f"STDOUT: {stdout.decode()}")
                print(f"STDERR: {stderr.decode()}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            return False
    
    def start_frontend(self):
        """Start the React frontend"""
        print("🎨 Starting Frontend...")
        frontend_path = Path(__file__).parent / "frontend" / "npc-dialogue-ai"
        
        if not frontend_path.exists():
            print("❌ Frontend directory not found!")
            return False
        
        try:
            os.chdir(frontend_path)
            
            # Check if node_modules exists
            if not (frontend_path / "node_modules").exists():
                print("📦 Installing frontend dependencies...")
                install_result = subprocess.run(["npm", "install"], 
                                              capture_output=True, text=True)
                if install_result.returncode != 0:
                    print(f"❌ Failed to install dependencies: {install_result.stderr}")
                    return False
            
            # Start the React development server
            self.frontend_process = subprocess.Popen(
                ["npm", "start"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            print("✅ Frontend starting on http://localhost:3000")
            return True
            
        except Exception as e:
            print(f"❌ Error starting frontend: {e}")
            return False
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n🛑 Shutting down system...")
        self.running = False
        
        if self.backend_process:
            self.backend_process.terminate()
        if self.frontend_process:
            self.frontend_process.terminate()
        
        sys.exit(0)
    
    def run(self):
        """Main run function"""
        print("🎮 NPC Dialogue Generator - System Startup")
        print("=" * 50)
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start backend
        if not self.start_backend():
            print("❌ Failed to start backend. Exiting.")
            return
        
        # Wait a bit for backend to fully start
        time.sleep(2)
        
        # Start frontend
        if not self.start_frontend():
            print("❌ Failed to start frontend. Backend is still running.")
            print("💡 You can access the API at http://localhost:8000")
            print("📚 API docs at http://localhost:8000/docs")
        
        print("\n🎉 System is running!")
        print("=" * 50)
        print("🌐 Frontend: http://localhost:3000")
        print("🔧 Backend: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("\n✨ Features Available:")
        print("  • Real-time dialogue with character consistency")
        print("  • Branching dialogue system")
        print("  • Translation (Spanish, French)")
        print("  • Interactive character selection")
        print("\n🛑 Press Ctrl+C to stop all services")
        
        try:
            # Keep running until interrupted
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    runner = SystemRunner()
    runner.run()

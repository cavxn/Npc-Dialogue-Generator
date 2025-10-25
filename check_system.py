#!/usr/bin/env python3
"""
System check script for NPC Dialogue Generator
Verifies all components are working correctly
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

def check_ports():
    """Check if ports are available"""
    print("🔍 Checking port availability...")
    
    try:
        # Check port 8000
        result = subprocess.run(["lsof", "-ti:8000"], capture_output=True, text=True)
        if result.stdout.strip():
            print("⚠️  Port 8000 is in use. Killing existing processes...")
            subprocess.run(["lsof", "-ti:8000", "|", "xargs", "kill", "-9"], shell=True)
            time.sleep(2)
        
        # Check port 3000
        result = subprocess.run(["lsof", "-ti:3000"], capture_output=True, text=True)
        if result.stdout.strip():
            print("⚠️  Port 3000 is in use. Killing existing processes...")
            subprocess.run(["lsof", "-ti:3000", "|", "xargs", "kill", "-9"], shell=True)
            time.sleep(2)
        
        print("✅ Ports are now available")
        return True
    except Exception as e:
        print(f"❌ Error checking ports: {e}")
        return False

def check_dependencies():
    """Check if all dependencies are installed"""
    print("📦 Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import openai
        import pydantic
        print("✅ All Python dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: python setup_complete.py")
        return False

def check_api_key():
    """Check if API key is configured"""
    print("🔑 Checking API key configuration...")
    
    env_path = Path("backend/.env")
    if not env_path.exists():
        print("❌ No .env file found")
        return False
    
    try:
        content = env_path.read_text()
        if "your_openai_api_key_here" in content:
            print("❌ OpenAI API key not configured")
            print("Please edit backend/.env and add your OpenAI API key")
            return False
        print("✅ API key is configured")
        return True
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def test_backend():
    """Test if backend starts correctly"""
    print("🚀 Testing backend startup...")
    
    try:
        # Start backend in background
        backend_path = Path(__file__).parent / "backend"
        os.chdir(backend_path)
        
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "simple_api:app", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for startup
        time.sleep(5)
        
        if process.poll() is None:
            # Test API endpoint
            try:
                response = requests.get("http://localhost:8000/", timeout=5)
                if response.status_code == 200:
                    print("✅ Backend is working correctly")
                    process.terminate()
                    return True
                else:
                    print(f"❌ Backend returned status {response.status_code}")
                    process.terminate()
                    return False
            except requests.exceptions.ConnectionError:
                print("❌ Backend is not responding")
                process.terminate()
                return False
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def test_frontend():
    """Test if frontend files exist"""
    print("🎨 Checking frontend files...")
    
    frontend_files = [
        "simple_frontend.html",
        "frontend/npc-dialogue-ai/src/App.js",
        "frontend/npc-dialogue-ai/src/pages/ChatBox.jsx"
    ]
    
    all_exist = True
    for file_path in frontend_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    """Main system check"""
    print("🧪 NPC Dialogue Generator - System Check")
    print("=" * 50)
    
    # Check ports
    if not check_ports():
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check API key
    if not check_api_key():
        return
    
    # Test backend
    if not test_backend():
        return
    
    # Test frontend
    if not test_frontend():
        return
    
    print("\n🎉 System Check Complete!")
    print("=" * 50)
    print("✅ All components are working correctly")
    print("\n🚀 Ready to start the system:")
    print("   python start.py")
    print("\n🌐 Or use the simple version:")
    print("   python start_simple.py")

if __name__ == "__main__":
    main()

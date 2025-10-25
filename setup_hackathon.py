#!/usr/bin/env python3
"""
Setup script for CodeZilla '25 Hackathon - NPC Dialogue Generator
Automatically sets up the environment and checks requirements
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def check_node_version():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js is not installed. Please install Node.js 16+ from https://nodejs.org/")
    return False

def install_python_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Python dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        return False

def install_frontend_dependencies():
    """Install frontend dependencies"""
    frontend_path = Path("frontend/npc-dialogue-ai")
    if not frontend_path.exists():
        print("❌ Frontend directory not found")
        return False
    
    print("📦 Installing frontend dependencies...")
    try:
        subprocess.run(["npm", "install"], cwd=frontend_path, check=True)
        print("✅ Frontend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install frontend dependencies")
        return False

def create_env_file():
    """Create .env file template"""
    env_path = Path("backend/.env")
    if env_path.exists():
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file template...")
    env_content = """# OpenAI API Key (required)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Google API Key for Gemini (if using)
# GOOGLE_API_KEY=your_google_api_key_here
"""
    
    try:
        env_path.parent.mkdir(exist_ok=True)
        env_path.write_text(env_content)
        print("✅ .env file created at backend/.env")
        print("⚠️  Please add your OpenAI API key to backend/.env")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_api_key():
    """Check if API key is configured"""
    env_path = Path("backend/.env")
    if not env_path.exists():
        return False
    
    try:
        content = env_path.read_text()
        if "your_openai_api_key_here" in content:
            print("⚠️  Please update your OpenAI API key in backend/.env")
            return False
        print("✅ API key appears to be configured")
        return True
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def main():
    """Main setup function"""
    print("🎮 CodeZilla '25 - NPC Dialogue Generator Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check Node.js
    if not check_node_version():
        return
    
    # Install Python dependencies
    if not install_python_dependencies():
        return
    
    # Install frontend dependencies
    if not install_frontend_dependencies():
        return
    
    # Create .env file
    if not create_env_file():
        return
    
    # Check API key
    api_configured = check_api_key()
    
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    
    if api_configured:
        print("✅ System is ready to run!")
        print("\n🚀 To start the system:")
        print("   python start_hackathon_system.py")
    else:
        print("⚠️  System setup complete, but API key needs configuration")
        print("\n📝 Next steps:")
        print("1. Get your OpenAI API key from https://platform.openai.com/api-keys")
        print("2. Update backend/.env with your API key")
        print("3. Run: python start_hackathon_system.py")
    
    print("\n🌐 Once running, visit: http://localhost:3000")
    print("📚 API docs available at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Complete setup script for NPC Dialogue Generator
Handles all setup requirements for the hackathon
"""

import subprocess
import sys
import os
from pathlib import Path

def install_python_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "fastapi", "uvicorn", "openai", "python-dotenv", "pydantic"
        ], check=True)
        print("✅ Python dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        return False

def create_env_file():
    """Create .env file template"""
    env_path = Path("backend/.env")
    if env_path.exists():
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file...")
    try:
        env_path.parent.mkdir(exist_ok=True)
        env_content = """# OpenAI API Key (required for dialogue generation)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Google API Key for Gemini (if using)
# GOOGLE_API_KEY=your_google_api_key_here
"""
        env_path.write_text(env_content)
        print("✅ .env file created at backend/.env")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def create_startup_script():
    """Create a simple startup script"""
    startup_content = '''#!/usr/bin/env python3
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
            
            print("\\n🎉 System is ready!")
            print("🌐 Frontend: simple_frontend.html")
            print("🔧 Backend: http://localhost:8000")
            print("📚 API Docs: http://localhost:8000/docs")
            print("\\n🛑 Press Ctrl+C to stop")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\\n👋 Shutting down...")
                process.terminate()
        else:
            print("❌ Backend failed to start")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
'''
    
    try:
        startup_path = Path("start.py")
        startup_path.write_text(startup_content)
        startup_path.chmod(0o755)
        print("✅ Startup script created")
        return True
    except Exception as e:
        print(f"❌ Failed to create startup script: {e}")
        return False

def main():
    """Main setup function"""
    print("🎮 NPC Dialogue Generator - Complete Setup")
    print("=" * 50)
    
    # Install Python dependencies
    if not install_python_dependencies():
        return
    
    # Create .env file
    if not create_env_file():
        return
    
    # Create startup script
    if not create_startup_script():
        return
    
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("📝 Next steps:")
    print("1. Get your OpenAI API key from https://platform.openai.com/api-keys")
    print("2. Edit backend/.env and replace 'your_openai_api_key_here' with your key")
    print("3. Run: python start.py")
    print("\n✨ Features:")
    print("  • Character creation and dialogue generation")
    print("  • Character consistency and memory")
    print("  • Branching dialogue system")
    print("  • Translation (Spanish, French)")
    print("  • Real-time interactive chat")

if __name__ == "__main__":
    main()

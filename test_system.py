#!/usr/bin/env python3
"""
Test script for the NPC Dialogue Generator system
Verifies all components are working correctly
"""

import requests
import json
import time
import sys
from pathlib import Path

def test_backend_health():
    """Test if the backend is running and healthy"""
    try:
        response = requests.get("http://localhost:8000/api/characters", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is running")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running. Please start it first.")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_character_creation():
    """Test character creation functionality"""
    try:
        character_data = {
            "name": "Test Warrior",
            "role": "Guardian",
            "personality": "Brave and protective",
            "backstory": "A seasoned warrior who protects the realm",
            "setting": "fantasy",
            "speaking_style": "formal and noble",
            "key_traits": "loyal, courageous, wise"
        }
        
        response = requests.post(
            "http://localhost:8000/api/character/create",
            json=character_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Character creation works")
            return data.get("character_id")
        else:
            print(f"❌ Character creation failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Character creation test failed: {e}")
        return None

def test_dialogue_generation(character_id):
    """Test dialogue generation"""
    try:
        dialogue_data = {
            "message": "Hello, how are you today?",
            "character_id": character_id,
            "session_id": "test_session"
        }
        
        response = requests.post(
            "http://localhost:8000/api/dialogue/generate",
            json=dialogue_data,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Dialogue generation works")
            print(f"   Character: {data.get('character_name')}")
            print(f"   Response: {data.get('response')[:100]}...")
            return True
        else:
            print(f"❌ Dialogue generation failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Dialogue generation test failed: {e}")
        return False

def test_branching_dialogue(character_id):
    """Test branching dialogue system"""
    try:
        branching_data = {
            "character_id": character_id,
            "session_id": "test_session",
            "selected_option": None
        }
        
        response = requests.post(
            "http://localhost:8000/api/dialogue/branching",
            json=branching_data,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Branching dialogue works")
            print(f"   Dialogue: {data.get('dialogue')[:100]}...")
            print(f"   Options: {len(data.get('options', []))} available")
            return True
        else:
            print(f"❌ Branching dialogue failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Branching dialogue test failed: {e}")
        return False

def test_translation():
    """Test translation functionality"""
    try:
        translation_data = {
            "text": "Hello, how are you today?",
            "target_language": "spanish"
        }
        
        response = requests.post(
            "http://localhost:8000/api/translate",
            json=translation_data,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Translation works")
            print(f"   Original: {data.get('original')}")
            print(f"   Translated: {data.get('translated')}")
            return True
        else:
            print(f"❌ Translation failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Translation test failed: {e}")
        return False

def test_frontend_files():
    """Test if frontend files exist and are properly structured"""
    frontend_path = Path("frontend/npc-dialogue-ai")
    
    required_files = [
        "package.json",
        "src/App.js",
        "src/pages/ChatBox.jsx",
        "src/pages/CharacterSelect.jsx",
        "src/pages/PersonalitySetup.jsx"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = frontend_path / file_path
        if full_path.exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("🧪 Testing NPC Dialogue Generator System")
    print("=" * 50)
    
    # Test frontend files
    print("\n📁 Testing Frontend Files...")
    if test_frontend_files():
        print("✅ Frontend structure is correct")
    else:
        print("❌ Frontend structure has issues")
        return
    
    # Test backend
    print("\n🔧 Testing Backend API...")
    if not test_backend_health():
        print("\n💡 To start the backend, run:")
        print("   cd backend && python -m uvicorn enhanced_dialogue_api:app --reload")
        return
    
    # Test character creation
    print("\n👤 Testing Character Creation...")
    character_id = test_character_creation()
    if not character_id:
        return
    
    # Test dialogue generation
    print("\n💬 Testing Dialogue Generation...")
    if not test_dialogue_generation(character_id):
        return
    
    # Test branching dialogue
    print("\n🌳 Testing Branching Dialogue...")
    if not test_branching_dialogue(character_id):
        return
    
    # Test translation
    print("\n🌍 Testing Translation...")
    if not test_translation():
        return
    
    print("\n🎉 All Tests Passed!")
    print("=" * 50)
    print("✅ System is ready for the hackathon!")
    print("\n🚀 To start the full system:")
    print("   python start_hackathon_system.py")
    print("\n🌐 Then visit: http://localhost:3000")

if __name__ == "__main__":
    main()

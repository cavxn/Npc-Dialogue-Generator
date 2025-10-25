#!/usr/bin/env python3
"""
Quick test to verify the backend API works
"""

import requests
import time
import sys

def test_backend():
    """Test if backend is running and working"""
    print("🧪 Testing Backend API...")
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/api/characters", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is running")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running")
        return False
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def test_character_creation():
    """Test character creation"""
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

def main():
    """Run quick tests"""
    print("🧪 Quick Backend Test")
    print("=" * 30)
    
    # Test backend health
    if not test_backend():
        print("\n💡 To start the backend manually:")
        print("   cd backend && python -m uvicorn enhanced_dialogue_api:app --reload")
        return
    
    # Test character creation
    print("\n👤 Testing Character Creation...")
    character_id = test_character_creation()
    if not character_id:
        return
    
    # Test dialogue generation
    print("\n💬 Testing Dialogue Generation...")
    if test_dialogue_generation(character_id):
        print("\n🎉 Backend is working correctly!")
        print("✅ Ready for hackathon submission!")
    else:
        print("\n❌ Backend has issues that need fixing")

if __name__ == "__main__":
    main()

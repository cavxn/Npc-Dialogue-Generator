from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import random
from datetime import datetime

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
conversations: Dict[str, List[Dict]] = {}
character_profiles: Dict[str, Dict] = {}

class CharacterProfile(BaseModel):
    name: str
    role: str
    personality: str
    backstory: str
    setting: str = "fantasy"
    speaking_style: str = "casual and friendly"
    key_traits: str = "helpful, knowledgeable"

class DialogueRequest(BaseModel):
    message: str
    character_id: str
    session_id: str

# Sample responses for different character types
SAMPLE_RESPONSES = {
    "warrior": [
        "I stand ready to defend this realm with honor!",
        "Your courage is admirable, traveler.",
        "The path ahead is dangerous, but together we are strong.",
        "I have seen many battles, and this one will be no different.",
        "Trust in your training, and victory will follow."
    ],
    "mage": [
        "The arcane energies flow through this place like a river.",
        "Knowledge is power, and power is responsibility.",
        "The ancient texts speak of times such as these.",
        "Magic is not to be taken lightly, young one.",
        "The mysteries of the universe are vast and wondrous."
    ],
    "merchant": [
        "Ah, a potential customer! What treasures can I show you?",
        "Business is good when travelers like yourself visit.",
        "I have the finest goods from across the realm.",
        "Quality comes at a price, but satisfaction is guaranteed.",
        "Let me tell you about this special item I have..."
    ],
    "guardian": [
        "I watch over this place, ensuring all who enter are safe.",
        "Your safety is my primary concern.",
        "I have sworn to protect those under my care.",
        "Vigilance is the key to preventing disaster.",
        "Rest assured, I will not let harm come to you."
    ],
    "default": [
        "Greetings, traveler! How may I assist you today?",
        "It's always a pleasure to meet new faces.",
        "I sense you have questions. Please, ask away.",
        "Welcome to our realm! I hope you find what you seek.",
        "The journey has brought you here for a reason."
    ]
}

def get_character_type(role: str) -> str:
    """Determine character type based on role"""
    role_lower = role.lower()
    if any(word in role_lower for word in ["warrior", "fighter", "knight", "guard"]):
        return "warrior"
    elif any(word in role_lower for word in ["mage", "wizard", "sorcerer", "magic"]):
        return "mage"
    elif any(word in role_lower for word in ["merchant", "trader", "vendor", "shop"]):
        return "merchant"
    elif any(word in role_lower for word in ["guardian", "protector", "keeper"]):
        return "guardian"
    else:
        return "default"

def generate_response(character: Dict, message: str) -> str:
    """Generate a simple response based on character type"""
    char_type = get_character_type(character.get("role", ""))
    responses = SAMPLE_RESPONSES.get(char_type, SAMPLE_RESPONSES["default"])
    
    # Add some context awareness
    message_lower = message.lower()
    if any(word in message_lower for word in ["hello", "hi", "greetings"]):
        return f"Greetings! I am {character['name']}, {character['role']}. {random.choice(responses)}"
    elif any(word in message_lower for word in ["help", "assist", "aid"]):
        return f"As {character['role']}, I am here to help. {random.choice(responses)}"
    elif any(word in message_lower for word in ["danger", "threat", "enemy"]):
        return f"I sense your concern about danger. {random.choice(responses)}"
    else:
        return f"{random.choice(responses)}"

@app.get("/api/characters")
def get_characters():
    """Get all character profiles"""
    return {"characters": list(character_profiles.values())}

@app.post("/api/character/create")
def create_character(profile: CharacterProfile):
    """Create a new character profile"""
    character_id = f"char_{len(character_profiles) + 1}"
    character_data = profile.dict()
    character_data["id"] = character_id
    character_profiles[character_id] = character_data
    
    return {
        "message": "Character created successfully",
        "character_id": character_id,
        "character": character_data
    }

@app.post("/api/dialogue/generate")
def generate_dialogue(request: DialogueRequest):
    """Generate dialogue response"""
    character_id = request.character_id
    session_key = f"{character_id}_{request.session_id}"
    
    if character_id not in character_profiles:
        raise HTTPException(status_code=404, detail="Character not found")
    
    character = character_profiles[character_id]
    
    # Generate response
    npc_response = generate_response(character, request.message)
    
    # Store conversation
    conversations[session_key] = conversations.get(session_key, []) + [
        {"speaker": "Player", "content": request.message, "timestamp": datetime.now().isoformat()},
        {"speaker": character["name"], "content": npc_response, "timestamp": datetime.now().isoformat()}
    ]
    
    return {
        "response": npc_response,
        "character_name": character["name"],
        "character_id": character_id,
        "session_id": request.session_id
    }

@app.get("/api/dialogue/history/{character_id}/{session_id}")
def get_conversation_history(character_id: str, session_id: str):
    """Get conversation history"""
    session_key = f"{character_id}_{session_id}"
    return {"conversation": conversations.get(session_key, [])}

@app.post("/api/dialogue/branching")
def create_branching_dialogue(request: dict):
    """Create branching dialogue options"""
    character_id = request.get("character_id")
    session_id = request.get("session_id")
    
    if character_id not in character_profiles:
        raise HTTPException(status_code=404, detail="Character not found")
    
    character = character_profiles[character_id]
    
    # Generate simple branching dialogue
    dialogue = f"{character['name']}: {generate_response(character, 'Tell me about your options')}"
    
    options = [
        {"id": "opt1", "text": "Tell me more about that"},
        {"id": "opt2", "text": "I have a different question"},
        {"id": "opt3", "text": "Thank you for your time"}
    ]
    
    return {
        "dialogue": dialogue,
        "options": options,
        "character_name": character["name"]
    }

@app.post("/api/translate")
def translate_dialogue(request: dict):
    """Simple translation (mock implementation)"""
    text = request.get("text", "")
    target_language = request.get("target_language", "spanish")
    
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    # Mock translation
    translated_text = f"[{target_language.upper()}] {text}"
    
    return {
        "original": text,
        "translated": translated_text,
        "target_language": target_language
    }

@app.get("/")
def root():
    return {"message": "NPC Dialogue Generator API - Simple Mode (No API Keys Required)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import os
from dotenv import load_dotenv
import openai

load_dotenv()

app = FastAPI(title="NPC Dialogue Generator", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai.api_key)

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

class BranchingDialogueRequest(BaseModel):
    character_id: str
    session_id: str
    selected_option: Optional[str] = None

def build_prompt(profile: dict, player_input: str = None, conversation_history: list = None):
    """Build a prompt for character-consistent dialogue generation"""
    prompt = f"""
You are an NPC in a {profile.get('setting', 'fantasy')} video game.

Character Name: {profile['name']}
Role: {profile['role']}
Personality: {profile['personality']}
Backstory: {profile['backstory']}
Speaking Style: {profile.get('speaking_style', 'casual and friendly')}
Key Traits: {profile.get('key_traits', 'helpful, knowledgeable')}

IMPORTANT: Maintain consistency in your character's voice, personality, and speaking patterns throughout the conversation. Stay in character at all times.

""".strip()

    # Add conversation history for context
    if conversation_history:
        prompt += "\n\nConversation History:\n"
        for msg in conversation_history[-5:]:  # Last 5 messages for context
            prompt += f"{msg['speaker']}: {msg['content']}\n"
        prompt += "\n"

    if player_input:
        prompt += f"\nPlayer: {player_input}\n{profile['name']} ({profile['role']}):"
    else:
        prompt += "\n\nIntroduce yourself to the player in character.\n"

    return prompt

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "NPC Dialogue Generator API",
        "version": "1.0.0",
        "endpoints": {
            "characters": "/api/characters",
            "create_character": "/api/character/create",
            "generate_dialogue": "/api/dialogue/generate",
            "branching_dialogue": "/api/dialogue/branching",
            "translate": "/api/translate"
        }
    }

@app.post("/api/character/create")
async def create_character(profile: CharacterProfile):
    """Create a new character profile"""
    character_id = f"char_{len(character_profiles) + 1}"
    character_data = profile.dict()
    character_profiles[character_id] = character_data
    return {"character_id": character_id, "profile": character_data}

@app.get("/api/characters")
async def get_characters():
    """Get all available characters"""
    return {"characters": character_profiles}

@app.post("/api/dialogue/generate")
async def generate_dialogue(request: DialogueRequest):
    """Generate dialogue with character consistency"""
    try:
        if request.character_id not in character_profiles:
            raise HTTPException(status_code=404, detail="Character not found")
        
        character = character_profiles[request.character_id]
        session_key = f"{request.character_id}_{request.session_id}"
        
        # Get conversation history
        conversation_history = conversations.get(session_key, [])
        
        # Build prompt with context
        prompt = build_prompt(character, request.message, conversation_history)
        
        # Generate response using OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert NPC dialogue generator. Maintain character consistency and provide engaging, immersive responses."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=300
        )
        
        npc_response = response.choices[0].message.content.strip()
        
        # Store conversation
        conversations[session_key] = conversations.get(session_key, []) + [
            {"speaker": "Player", "content": request.message, "timestamp": "now"},
            {"speaker": character["name"], "content": npc_response, "timestamp": "now"}
        ]
        
        return {
            "response": npc_response,
            "character_name": character["name"],
            "session_id": request.session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/dialogue/branching")
async def generate_branching_dialogue(request: BranchingDialogueRequest):
    """Generate branching dialogue with multiple conversation paths"""
    try:
        if request.character_id not in character_profiles:
            raise HTTPException(status_code=404, detail="Character not found")
        
        character = character_profiles[request.character_id]
        
        # Create branching dialogue structure
        if not request.selected_option:
            # Initial dialogue with options
            prompt = f"""
            Create a branching dialogue for {character['name']}, a {character['role']} in a {character['setting']} setting.
            Character personality: {character['personality']}
            Backstory: {character['backstory']}
            
            Create an engaging opening dialogue with 3-4 conversation options for the player.
            Format the response as:
            DIALOGUE: [character's opening dialogue]
            OPTION1: [first option text]
            OPTION2: [second option text]
            OPTION3: [third option text]
            OPTION4: [fourth option text]
            """
        else:
            # Follow-up based on selected option
            prompt = f"""
            Continue the conversation as {character['name']} responding to the player's choice: "{request.selected_option}"
            Maintain character consistency and provide 2-3 new conversation options.
            Format as:
            DIALOGUE: [character's response]
            OPTION1: [first option text]
            OPTION2: [second option text]
            OPTION3: [third option text]
            """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert game dialogue writer. Create engaging, branching conversations that maintain character consistency."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=400
        )
        
        dialogue_text = response.choices[0].message.content.strip()
        
        # Parse the response to extract dialogue and options
        lines = dialogue_text.split('\n')
        dialogue = ""
        options = []
        
        for line in lines:
            if line.startswith('DIALOGUE:'):
                dialogue = line.replace('DIALOGUE:', '').strip()
            elif line.startswith('OPTION'):
                options.append(line.split(':', 1)[1].strip())
        
        return {
            "dialogue": dialogue,
            "options": options,
            "character_name": character["name"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/translate")
async def translate_dialogue(request: dict):
    """Translate dialogue to different languages"""
    try:
        text = request.get("text", "")
        target_language = request.get("target_language", "spanish")
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Translate the following text to {target_language}. Maintain the tone and style of the original text."},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        translated_text = response.choices[0].message.content.strip()
        
        return {
            "original": text,
            "translated": translated_text,
            "target_language": target_language
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversation/{character_id}/{session_id}")
async def get_conversation(character_id: str, session_id: str):
    """Get conversation history"""
    session_key = f"{character_id}_{session_id}"
    return {"conversation": conversations.get(session_key, [])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

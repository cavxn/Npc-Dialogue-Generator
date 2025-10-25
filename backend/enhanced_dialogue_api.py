from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai
try:
    from prompt_builder import build_prompt
except ImportError:
    # Fallback if prompt_builder is not available
    def build_prompt(profile: dict, player_input: str = None, conversation_history: list = None):
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

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Google API key not found. Set GOOGLE_API_KEY in .env file.")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# In-memory storage for conversations and character profiles
conversations: Dict[str, List[Dict]] = {}
character_profiles: Dict[str, Dict] = {}
active_connections: Dict[str, WebSocket] = {}

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

class BranchingOption(BaseModel):
    text: str
    next_node_id: str

class DialogueNode(BaseModel):
    id: str
    text: str
    options: List[BranchingOption] = []
    is_end: bool = False

class BranchingDialogueRequest(BaseModel):
    character_id: str
    session_id: str
    selected_option: Optional[str] = None

@app.post("/api/character/create")
async def create_character(profile: CharacterProfile):
    """Create a new character profile"""
    character_id = f"char_{len(character_profiles) + 1}"
    character_data = profile.dict()
    character_profiles[character_id] = character_data
    return {"character_id": character_id, "profile": character_data}

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
        
        # Generate response using Gemini
        try:
            response = model.generate_content(
                f"You are an expert NPC dialogue generator. Maintain character consistency and provide engaging, immersive responses.\n\n{prompt}",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=300,
                    temperature=0.8
                )
            )
            npc_response = response.text.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating dialogue: {str(e)}")
        
        # Store conversation
        conversations[session_key] = conversations.get(session_key, []) + [
            {"speaker": "Player", "content": request.message, "timestamp": datetime.now().isoformat()},
            {"speaker": character["name"], "content": npc_response, "timestamp": datetime.now().isoformat()}
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
        
        try:
            response = model.generate_content(
                f"You are an expert game dialogue writer. Create engaging, branching conversations that maintain character consistency.\n\n{prompt}",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=400,
                    temperature=0.8
                )
            )
            dialogue_text = response.text.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating branching dialogue: {str(e)}")
        
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
        
        try:
            response = model.generate_content(
                f"Translate the following text to {target_language}. Maintain the tone and style of the original text.\n\n{text}",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=200,
                    temperature=0.3
                )
            )
            translated_text = response.text.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error translating text: {str(e)}")
        
        return {
            "original": text,
            "translated": translated_text,
            "target_language": target_language
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/{character_id}/{session_id}")
async def websocket_endpoint(websocket: WebSocket, character_id: str, session_id: str):
    """WebSocket endpoint for real-time dialogue"""
    await websocket.accept()
    active_connections[f"{character_id}_{session_id}"] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Generate response
            request = DialogueRequest(
                message=message_data["message"],
                character_id=character_id,
                session_id=session_id
            )
            
            response = await generate_dialogue(request)
            
            # Send response back through WebSocket
            await websocket.send_text(json.dumps(response))
            
    except WebSocketDisconnect:
        if f"{character_id}_{session_id}" in active_connections:
            del active_connections[f"{character_id}_{session_id}"]

@app.get("/api/characters")
async def get_characters():
    """Get all available characters"""
    return {"characters": character_profiles}

@app.get("/api/conversation/{character_id}/{session_id}")
async def get_conversation(character_id: str, session_id: str):
    """Get conversation history"""
    session_key = f"{character_id}_{session_id}"
    return {"conversation": conversations.get(session_key, [])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

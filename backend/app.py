from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import json

app = FastAPI()

# Allow frontend origin (adjust if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DialogueRequest(BaseModel):
    player_message: str
    npc_role: str

@app.post("/api/generate")
async def generate_dialogue(request: DialogueRequest):
    prompt = f"You are an NPC in a video game. Your role is: {request.npc_role}.\n" \
             f"A player says: \"{request.player_message}\"\nRespond like an NPC would:"
    
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout.strip()
        return {"response": output}
    except Exception as e:
        return {"error": str(e)}

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dialogue_gen import generate_dialogue as generate_response
from prompt_builder import build_prompt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DialogueRequest(BaseModel):
    player_input: str
    npc_role: str

# Sample profiles per role
npc_profiles = {
    "Blacksmith": {
        "name": "Gorim",
        "role": "Blacksmith",
        "setting": "medieval fantasy",
        "personality": "Gruff but kind-hearted. Speaks bluntly. Loves his craft.",
        "backstory": "Gorim has been forging weapons for over 30 years. He lost his brother to a dragon and now helps adventurers gear up to slay beasts."
    },
    "Wizard": {
        "name": "Elarion",
        "role": "Wizard",
        "setting": "medieval fantasy",
        "personality": "Wise and mysterious. Speaks in riddles sometimes.",
        "backstory": "Once a court wizard, Elarion now wanders the realm in search of arcane relics."
    },
    # Add more NPC types here if needed
}

@app.get("/")
def read_root():
    return {"message": "NPC Dialogue Generator API running!"}

@app.post("/generate_dialogue")
def generate_dialogue(request: DialogueRequest):
    profile = npc_profiles.get(request.npc_role, {
        "name": request.npc_role,
        "role": request.npc_role,
        "setting": "fantasy",
        "personality": "Neutral",
        "backstory": "No specific backstory."
    })

    prompt = build_prompt(profile, player_input=request.player_input)
    npc_response = generate_response(prompt)
    return {"npc_response": npc_response}

# gemini_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Google API key not found. Set GOOGLE_API_KEY in .env file.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

app = FastAPI()

# Allow requests from frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    user_input: str

chat_sessions = {}

@app.post("/chat")
def chat(message: Message):
    session_id = "default"  # For now, single session
    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat()

    try:
        convo = chat_sessions[session_id]
        convo.send_message(message.user_input)
        return {"response": convo.last.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

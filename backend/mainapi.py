from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Ensure key is present
if not GOOGLE_API_KEY:
    raise ValueError("❌ Google API key not found. Please set it in a `.env` file.")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Initialize FastAPI
app = FastAPI()

# Enable CORS (for frontend to access this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chat sessions
chat_sessions = {}

# Request schema
class ChatRequest(BaseModel):
    session_id: str
    message: str

# Response schema
class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    session_id = req.session_id

    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat()

    try:
        response = chat_sessions[session_id].send_message(req.message)
        return ChatResponse(reply=response.text)
    except Exception as e:
        return ChatResponse(reply=f"❌ Error: {str(e)}")

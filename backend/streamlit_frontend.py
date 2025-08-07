import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Ensure key is present
if not GOOGLE_API_KEY:
    st.error("❌ Google API key not found. Please set it in a `.env` file.")
    st.stop()

# Configure the Gemini model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# Initialize chat session in Streamlit
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()
    st.session_state.messages = []

# Streamlit UI
st.title("🧠 Gemini Chatbot")
st.markdown("Chat with Gemini (powered by Google Generative AI)")

# Display previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Input box
user_input = st.chat_input("Say something to Gemini...")

# If user sends a message
if user_input:
    # Show user's message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Get Gemini response
        response = st.session_state.chat.send_message(user_input)
        bot_reply = response.text
        st.chat_message("assistant").markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    except Exception as e:
        st.error(f"❌ Gemini failed to respond: {e}")

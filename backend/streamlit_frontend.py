import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# ---------- Load API Key from .env ----------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ Google API key not found. Please set it in a `.env` file.")
    st.stop()

# ---------- Configure Gemini Model ----------
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# ---------- Initialize Chat State ----------
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()
    st.session_state.messages = []

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Gemini Chatbot", page_icon="🧠")
st.title("🧠 Gemini Chatbot")
st.markdown("Chat with Gemini (powered by Google Generative AI)")

# Display chat history
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

# ---------- Handle User Input ----------
user_input = st.chat_input("Say something to Gemini...")

if user_input:
    # Show user's message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        # Generate response from Gemini
        response = st.session_state.chat.send_message(user_input)
        bot_reply = response.text

        st.chat_message("assistant").markdown(bot_reply)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        st.error(f"❌ Gemini failed to respond: {e}")

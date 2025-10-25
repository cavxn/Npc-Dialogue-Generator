import streamlit as st
import pyttsx3
import google.generativeai as genai

# ---- SETUP GEMINI API KEY ----
genai.configure(api_key="AIzaSyB8QviSIdb-uYTdXo0D8v4fCo7-8ZSJ_us")

model = genai.GenerativeModel("gemini-pro")

# ---- TEXT-TO-SPEECH INIT ----
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---- STREAMLIT APP ----
st.set_page_config(page_title="Game Character Roleplay", layout="centered")
st.title("🎮 AI Game Character Dialogue")

user_input = st.text_input("🧠 Say something to the character:", "")

if st.button("Talk to AI Character") and user_input:
    with st.spinner("Thinking..."):
        try:
            response = model.generate_content(user_input)
            reply = response.text.strip()
            st.markdown("**💬 AI Response:**")
            st.success(reply)
            speak(reply)
        except Exception as e:
            st.error(f"Error: {e}")

import streamlit as st
import requests
import pyttsx3

# Character voices (can customize more later)
CHARACTER_VOICES = {
    "Knight": {"voice": 0},
    "Wizard": {"voice": 1},
    "Rogue": {"voice": 2},
    "Priestess": {"voice": 3},
}

EMOTIONS = ["Happy", "Sad", "Angry", "Curious", "Worried"]
BACKEND_URL = "http://127.0.0.1:8000"

engine = pyttsx3.init()

def set_voice(voice_id):
    voices = engine.getProperty('voices')
    if voice_id < len(voices):
        engine.setProperty('voice', voices[voice_id].id)

def speak_text(text, voice_id=0):
    set_voice(voice_id)
    engine.say(text)
    engine.runAndWait()

# --- UI ---
st.title("🎮 NPC Dialogue Generator with Voice")

character = st.selectbox("Choose character", list(CHARACTER_VOICES.keys()))
emotion = st.selectbox("Choose emotion", EMOTIONS)
user_input = st.text_input("What should the character say?")

if st.button("🎤 Generate Dialogue"):
    if user_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        prompt = f"{character} feels {emotion.lower()} and says: {user_input}"
        try:
            response = requests.post(BACKEND_URL, json={"prompt": prompt})
            data = response.json()
            reply = data.get("response", "No response from backend.")
        except Exception as e:
            reply = f"❌ Error: {e}"

        st.markdown(f"**🧠 AI Response:** {reply}")
        speak_text(reply, CHARACTER_VOICES[character]["voice"])

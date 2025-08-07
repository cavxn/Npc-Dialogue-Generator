import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env from project root or same directory
load_dotenv()

# Safely load API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# Create client
client = OpenAI(api_key=api_key)


def generate_dialogue(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an NPC in a fantasy world responding to a player."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=250
    )
    return response.choices[0].message.content.strip()

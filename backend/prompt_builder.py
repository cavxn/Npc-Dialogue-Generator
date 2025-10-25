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

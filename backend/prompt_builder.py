def build_prompt(profile: dict, player_input: str = None):
    prompt = f"""
You are an NPC in a {profile['setting']} video game.

Character Name: {profile['name']}
Role: {profile['role']}
Personality: {profile['personality']}
Backstory: {profile['backstory']}

Speak like this NPC would.
""".strip()

    if player_input:
        prompt += f"\n\nPlayer: {player_input}\n{profile['name']} ({profile['role']}):"
    else:
        prompt += "\n\nIntroduce yourself to the player.\n"

    return prompt

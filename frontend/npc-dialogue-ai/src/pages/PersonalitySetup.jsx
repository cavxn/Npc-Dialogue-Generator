// src/pages/PersonalitySetup.jsx
import React, { useState } from "react";
import './PersonalitySetup.css';

const PERSONALITY_TRAITS = [
  "Sarcastic", "Helpful", "Aggressive", "Nervous", "Calm", "Witty", "Mysterious"
];

const EMOTIONAL_TONES = [
  "Happy", "Angry", "Scared", "Neutral", "Sad", "Excited"
];

export default function PersonalitySetup({ selectedCharacter, onConfirm }) {
  const [selectedTraits, setSelectedTraits] = useState([]);
  const [emotionalTone, setEmotionalTone] = useState("Neutral");
  const [backstory, setBackstory] = useState("");

  const toggleTrait = (trait) => {
    setSelectedTraits((prev) =>
      prev.includes(trait) ? prev.filter((t) => t !== trait) : [...prev, trait]
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const npcPersonality = {
      traits: selectedTraits,
      emotion: emotionalTone,
      backstory,
    };

    console.log("✅ Final NPC Profile:", {
      character: selectedCharacter,
      ...npcPersonality,
    });

    // move to ChatBox by calling onConfirm and passing a stringified summary
    const personalitySummary = `
${selectedCharacter.name} is a ${emotionalTone} character with traits like ${selectedTraits.join(', ') || 'none'}.
Backstory: ${backstory || 'No backstory provided.'}
    `.trim();

    onConfirm(personalitySummary); // <<--- this triggers ChatBox in App.jsx
  };

  return (
    <div className="setup-container">
      <video autoPlay loop muted className="background-video">
        <source src="/video2.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      <div className="setup-card">
        {selectedCharacter?.avatar && (
          <div className="character-preview">
            <img src={selectedCharacter.avatar} alt={selectedCharacter.name} />
            <h2>{selectedCharacter.name}</h2>
          </div>
        )}

        <h1>🧠 Personality & Emotion Setup</h1>

        <div>
          <label className="label">Choose Personality Traits:</label>
          <div className="traits-container">
            {PERSONALITY_TRAITS.map((trait) => (
              <button
                key={trait}
                onClick={() => toggleTrait(trait)}
                className={`trait-button ${selectedTraits.includes(trait) ? 'selected' : ''}`}
              >
                {trait}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="label">Select Mood / Emotional Tone:</label>
          <select
            value={emotionalTone}
            onChange={(e) => setEmotionalTone(e.target.value)}
          >
            {EMOTIONAL_TONES.map((tone) => (
              <option key={tone} value={tone}>{tone}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="label">Optional: Backstory or Goals</label>
          <textarea
            rows={4}
            placeholder="Why this character matters..."
            value={backstory}
            onChange={(e) => setBackstory(e.target.value)}
          />
        </div>

        <button onClick={handleSubmit} className="submit-button">
          ✅ Generate NPC
        </button>
      </div>
    </div>
  );
}

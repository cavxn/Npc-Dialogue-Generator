// src/components/DialogueGenerator.jsx
import React, { useState } from 'react';
import './DialogueGenerator.css';

const DialogueGenerator = () => {
  const [scenario, setScenario] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!scenario.trim()) return;
    setLoading(true);
    setResponse('');

    try {
      const res = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: scenario }),
      });

      const data = await res.json();
      setResponse(data.generated_dialogue || 'No response received.');
    } catch (error) {
      setResponse('Error: Unable to generate dialogue.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dialogue-container">
      <h2>🎭 Dialogue Generator</h2>
      <textarea
        className="glow-box"
        placeholder="Enter scenario, player action, or context..."
        value={scenario}
        onChange={(e) => setScenario(e.target.value)}
      />

      <button className="generate-btn" onClick={handleGenerate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Response'}
      </button>

      {response && (
        <div className="response-box">
          <strong>NPC:</strong> {response}
        </div>
      )}
    </div>
  );
};

export default DialogueGenerator;

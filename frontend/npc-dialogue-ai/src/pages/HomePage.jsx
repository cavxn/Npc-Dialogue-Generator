import React, { useState, useEffect } from 'react';
import './homepage.css';

const HomePage = ({ onStart }) => {
  const [currentFeature, setCurrentFeature] = useState(0);
  const [isVisible, setIsVisible] = useState(false);

  const features = [
    "🗣️ Personality Engine – Tailored dialogue per NPC type",
    "🔁 Consistency – Keeps NPC voice intact over long quests", 
    "🎮 Real-time Talk – Reacts to player choices instantly",
    "🌿 Branching Logic – Endless narrative possibilities",
    "🌍 Multi-language – Talk to your NPCs in any language!"
  ];

  useEffect(() => {
    setIsVisible(true);
    const interval = setInterval(() => {
      setCurrentFeature((prev) => (prev + 1) % features.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className={`home-container ${isVisible ? 'visible' : ''}`}>
      {/* Background video */}
      <video className="bg-video" autoPlay muted loop playsInline>
        <source src="/videoooooooo.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      {/* Dark overlay */}
      <div className="bg-overlay"></div>

      {/* Centered Glass Card */}
      <div className="glass-card centered-card">
        <h1 className="glow">🎮 AI NPC Dialogue Generator</h1>
        <p className="subtitle">Let your characters talk, think, and surprise players 🤖✨</p>

        <div className="typing-effect">
          <p>
            Power your virtual worlds with intelligent NPC dialogue.<br />
            Generate conversations that feel alive and connected.
          </p>
        </div>

        <div className="features">
          <h2 className="glow-small">✨ Features</h2>
          <div className="feature-showcase">
            <div className="feature-display">
              {features[currentFeature]}
            </div>
            <div className="feature-dots">
              {features.map((_, index) => (
                <span 
                  key={index}
                  className={`dot ${index === currentFeature ? 'active' : ''}`}
                />
              ))}
            </div>
          </div>
          <ul className="feature-list">
            <li>🗣️ <strong>Personality Engine</strong> – Tailored dialogue per NPC type</li>
            <li>🔁 <strong>Consistency</strong> – Keeps NPC voice intact over long quests</li>
            <li>🎮 <strong>Real-time Talk</strong> – Reacts to player choices instantly</li>
            <li>🌿 <strong>Branching Logic</strong> – Endless narrative possibilities</li>
            <li>🌍 <strong>Multi-language</strong> – Talk to your NPCs in any language!</li>
          </ul>
        </div>

        <button className="start-button" onClick={onStart}>
          🚀 Start Creating NPC Dialogue
        </button>

        <p className="footer-quote">“A good NPC isn't just a character — it's a storyteller.” 🌟</p>
      </div>
    </div>
  );
};

export default HomePage;

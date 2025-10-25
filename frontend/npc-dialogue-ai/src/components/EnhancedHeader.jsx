import React, { useState, useEffect } from 'react';
import './EnhancedHeader.css';

const EnhancedHeader = ({ character, onBack, onSettings }) => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const checkConnection = () => {
      fetch('http://localhost:8000/api/characters')
        .then(() => setIsOnline(true))
        .catch(() => setIsOnline(false));
    };

    checkConnection();
    const interval = setInterval(checkConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="enhanced-header">
      <div className="header-left">
        <button className="back-button" onClick={onBack}>
          ← Back
        </button>
        <div className="character-info">
          {character && (
            <>
              <div className="character-avatar">
                <span className="avatar-emoji">🤖</span>
                <div className={`status-indicator ${isOnline ? 'online' : 'offline'}`}></div>
              </div>
              <div className="character-details">
                <h3>{character.name}</h3>
                <p>{character.desc}</p>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="header-center">
        <div className="session-info">
          <span className="session-id">Session: {Date.now().toString().slice(-6)}</span>
          <span className="connection-status">
            {isOnline ? '🟢 Connected' : '🔴 Disconnected'}
          </span>
        </div>
      </div>

      <div className="header-right">
        <div className="time-display">
          {currentTime.toLocaleTimeString()}
        </div>
        <div className="header-actions">
          <button className="settings-button" onClick={onSettings}>
            ⚙️
          </button>
          <button className="help-button">
            ❓
          </button>
        </div>
      </div>
    </div>
  );
};

export default EnhancedHeader;

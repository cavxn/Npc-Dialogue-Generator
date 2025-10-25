import React, { useState } from 'react';
import './MessageBubble.css';

const MessageBubble = ({ message, character, onTranslate, onRegenerate }) => {
  const [showActions, setShowActions] = useState(false);
  const [isTranslating, setIsTranslating] = useState(false);

  const handleTranslate = async (language) => {
    setIsTranslating(true);
    try {
      await onTranslate(message.id, language);
    } finally {
      setIsTranslating(false);
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div 
      className={`message-bubble ${message.type}`}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      <div className="message-header">
        <div className="message-sender">
          <span className="sender-avatar">
            {message.type === 'player' ? '👤' : '🤖'}
          </span>
          <span className="sender-name">
            {message.type === 'player' ? 'You' : character?.name}
          </span>
        </div>
        <div className="message-time">
          {formatTime(message.timestamp)}
        </div>
      </div>

      <div className="message-content">
        <p>{message.content}</p>
        
        {message.translation && (
          <div className="translation-display">
            <div className="translation-header">
              <span className="translation-flag">
                {message.translatedLanguage === 'spanish' ? '🇪🇸' : 
                 message.translatedLanguage === 'french' ? '🇫🇷' : '🌍'}
              </span>
              <span className="translation-label">
                {message.translatedLanguage?.toUpperCase()}
              </span>
            </div>
            <p className="translated-text">{message.translation}</p>
          </div>
        )}
      </div>

      <div className={`message-actions ${showActions ? 'visible' : ''}`}>
        <div className="action-buttons">
          <button 
            className="action-btn translate-btn"
            onClick={() => handleTranslate('spanish')}
            disabled={isTranslating}
            title="Translate to Spanish"
          >
            🇪🇸
          </button>
          <button 
            className="action-btn translate-btn"
            onClick={() => handleTranslate('french')}
            disabled={isTranslating}
            title="Translate to French"
          >
            🇫🇷
          </button>
          <button 
            className="action-btn copy-btn"
            onClick={() => navigator.clipboard.writeText(message.content)}
            title="Copy message"
          >
            📋
          </button>
          {message.type === 'npc' && onRegenerate && (
            <button 
              className="action-btn regenerate-btn"
              onClick={() => onRegenerate(message.id)}
              title="Regenerate response"
            >
              🔄
            </button>
          )}
        </div>
      </div>

      {isTranslating && (
        <div className="translating-indicator">
          <span className="spinner"></span>
          <span>Translating...</span>
        </div>
      )}
    </div>
  );
};

export default MessageBubble;

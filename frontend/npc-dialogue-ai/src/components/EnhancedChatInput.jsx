import React, { useState, useRef, useEffect } from 'react';
import './EnhancedChatInput.css';

const EnhancedChatInput = ({ 
  onSendMessage, 
  isLoading, 
  dialogueMode, 
  branchingOptions, 
  onOptionSelect,
  placeholder 
}) => {
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const inputRef = useRef(null);
  const typingTimeoutRef = useRef(null);

  const quickSuggestions = [
    "Hello, how are you?",
    "Tell me about yourself",
    "What can you help me with?",
    "What's your story?",
    "How do you feel about this situation?"
  ];

  useEffect(() => {
    if (isTyping) {
      inputRef.current?.focus();
    }
  }, [isTyping]);

  const handleInputChange = (e) => {
    const value = e.target.value;
    setInputValue(value);
    
    // Clear existing timeout
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }
    
    // Set new timeout for suggestions
    if (value.length > 2) {
      typingTimeoutRef.current = setTimeout(() => {
        const filtered = quickSuggestions.filter(suggestion =>
          suggestion.toLowerCase().includes(value.toLowerCase())
        );
        setSuggestions(filtered.slice(0, 3));
      }, 300);
    } else {
      setSuggestions([]);
    }
  };

  const handleSend = () => {
    if (inputValue.trim() && !isLoading) {
      onSendMessage(inputValue);
      setInputValue('');
      setSuggestions([]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInputValue(suggestion);
    setSuggestions([]);
    inputRef.current?.focus();
  };

  const handleQuickAction = (action) => {
    setInputValue(action);
    inputRef.current?.focus();
  };

  return (
    <div className="enhanced-chat-input">
      {/* Quick Action Buttons */}
      <div className="quick-actions">
        <button 
          className="quick-action-btn"
          onClick={() => handleQuickAction("Hello!")}
          disabled={isLoading}
        >
          👋 Greet
        </button>
        <button 
          className="quick-action-btn"
          onClick={() => handleQuickAction("Tell me about your background")}
          disabled={isLoading}
        >
          📖 Background
        </button>
        <button 
          className="quick-action-btn"
          onClick={() => handleQuickAction("What are your thoughts on this?")}
          disabled={isLoading}
        >
          💭 Thoughts
        </button>
        <button 
          className="quick-action-btn"
          onClick={() => handleQuickAction("How can you help me?")}
          disabled={isLoading}
        >
          🤝 Help
        </button>
      </div>

      {/* Branching Options */}
      {branchingOptions.length > 0 && (
        <div className="branching-options">
          <h4>Choose your response:</h4>
          <div className="options-grid">
            {branchingOptions.map((option, index) => (
              <button 
                key={index}
                className="option-button"
                onClick={() => onOptionSelect(option)}
                disabled={isLoading}
              >
                {option}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Main Input Area */}
      <div className="input-container">
        <div className="input-wrapper">
          <textarea
            ref={inputRef}
            value={inputValue}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            placeholder={placeholder || "Type your message..."}
            disabled={isLoading}
            className="message-input"
            rows="1"
            onFocus={() => setIsTyping(true)}
            onBlur={() => {
              setTimeout(() => setIsTyping(false), 200);
            }}
          />
          
          <div className="input-actions">
            <button 
              className="send-button"
              onClick={handleSend}
              disabled={!inputValue.trim() || isLoading}
            >
              {isLoading ? (
                <span className="loading-spinner">⏳</span>
              ) : (
                '🚀'
              )}
            </button>
          </div>
        </div>

        {/* Suggestions Dropdown */}
        {suggestions.length > 0 && (
          <div className="suggestions-dropdown">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                className="suggestion-item"
                onClick={() => handleSuggestionClick(suggestion)}
              >
                💡 {suggestion}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Input Status */}
      <div className="input-status">
        <span className="character-count">
          {inputValue.length}/500
        </span>
        <span className="mode-indicator">
          {dialogueMode === 'freeform' ? '💬 Free Chat' : '🌿 Branching'}
        </span>
      </div>
    </div>
  );
};

export default EnhancedChatInput;

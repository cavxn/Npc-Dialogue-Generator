import React, { useState, useEffect, useRef, useCallback } from "react";
import EnhancedHeader from '../components/EnhancedHeader';
import MessageBubble from '../components/MessageBubble';
import EnhancedChatInput from '../components/EnhancedChatInput';
import './EnhancedChatBox.css';

const EnhancedChatBox = ({ character, personality, onBack }) => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [dialogueMode, setDialogueMode] = useState("freeform");
  const [branchingOptions, setBranchingOptions] = useState([]);
  const [sessionId] = useState(() => Date.now().toString());
  const [characterId, setCharacterId] = useState(null);
  const [ws, setWs] = useState(null);
  const [showSettings, setShowSettings] = useState(false);
  const [typingIndicator, setTypingIndicator] = useState(false);
  const messagesEndRef = useRef(null);
  const typingTimeoutRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (character && personality) {
      createCharacterProfile();
    }
  }, [character, personality]);

  const createCharacterProfile = useCallback(async () => {
    try {
      const response = await fetch("http://localhost:8000/api/character/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: character.name,
          role: character.desc,
          personality: personality,
          backstory: character.detail,
          setting: "sci-fi",
          speaking_style: "engaging and immersive",
          key_traits: "helpful, knowledgeable, engaging"
        })
      });
      
      const data = await response.json();
      setCharacterId(data.character_id);
      
      // Initialize conversation with enhanced welcome
      const welcomeMessage = {
        id: Date.now(),
        type: "npc",
        content: `Greetings! I'm ${character.name}, ${character.desc}. I'm here to assist you in any way I can. What would you like to know or discuss?`,
        timestamp: new Date().toISOString()
      };
      setMessages([welcomeMessage]);
    } catch (error) {
      console.error("Error creating character:", error);
    }
  }, [character, personality]);

  const connectWebSocket = useCallback(() => {
    if (characterId && sessionId) {
      const websocket = new WebSocket(`ws://localhost:8000/ws/${characterId}/${sessionId}`);
      
      websocket.onopen = () => {
        console.log("WebSocket connected");
        setWs(websocket);
      };
      
      websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const npcMessage = {
          id: Date.now(),
          type: "npc",
          content: data.response,
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, npcMessage]);
        setIsLoading(false);
        setTypingIndicator(false);
      };
      
      websocket.onclose = () => {
        console.log("WebSocket disconnected");
        setWs(null);
      };
    }
  }, [characterId, sessionId]);

  useEffect(() => {
    if (characterId) {
      connectWebSocket();
    }
  }, [characterId, connectWebSocket]);

  const handleSendMessage = async (messageText) => {
    if (!messageText.trim() || !characterId) return;

    const playerMessage = {
      id: Date.now(),
      type: "player",
      content: messageText,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, playerMessage]);
    setIsLoading(true);
    setTypingIndicator(true);

    // Clear typing indicator after delay
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }
    typingTimeoutRef.current = setTimeout(() => {
      setTypingIndicator(false);
    }, 3000);

    if (dialogueMode === "freeform") {
      if (ws) {
        ws.send(JSON.stringify({ message: messageText }));
      } else {
        try {
          const response = await fetch("http://localhost:8000/api/dialogue/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              message: messageText,
              character_id: characterId,
              session_id: sessionId
            })
          });
          
          const data = await response.json();
          const npcMessage = {
            id: Date.now(),
            type: "npc",
            content: data.response,
            timestamp: new Date().toISOString()
          };
          setMessages(prev => [...prev, npcMessage]);
        } catch (error) {
          console.error("Error sending message:", error);
        }
        setIsLoading(false);
        setTypingIndicator(false);
      }
    } else {
      try {
        const response = await fetch("http://localhost:8000/api/dialogue/branching", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            character_id: characterId,
            session_id: sessionId,
            selected_option: messageText
          })
        });
        
        const data = await response.json();
        const npcMessage = {
          id: Date.now(),
          type: "npc",
          content: data.dialogue,
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, npcMessage]);
        
        if (data.options && data.options.length > 0) {
          setBranchingOptions(data.options);
        }
      } catch (error) {
        console.error("Error with branching dialogue:", error);
      }
      setIsLoading(false);
      setTypingIndicator(false);
    }
  };

  const handleOptionSelect = (option) => {
    setBranchingOptions([]);
    handleSendMessage(option);
  };

  const translateMessage = async (messageId, targetLanguage = "spanish") => {
    try {
      const message = messages.find(m => m.id === messageId);
      if (!message) return;

      const response = await fetch("http://localhost:8000/api/translate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: message.content,
          target_language: targetLanguage
        })
      });
      
      const data = await response.json();
      
      setMessages(prev => prev.map(m => 
        m.id === messageId 
          ? { ...m, translation: data.translated, translatedLanguage: targetLanguage }
          : m
      ));
    } catch (error) {
      console.error("Error translating message:", error);
    }
  };

  const regenerateMessage = async (messageId) => {
    try {
      const message = messages.find(m => m.id === messageId);
      if (!message || message.type !== 'npc') return;

      const response = await fetch("http://localhost:8000/api/dialogue/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: "Please provide an alternative response to the previous message",
          character_id: characterId,
          session_id: sessionId
        })
      });
      
      const data = await response.json();
      
      setMessages(prev => prev.map(m => 
        m.id === messageId 
          ? { ...m, content: data.response }
          : m
      ));
    } catch (error) {
      console.error("Error regenerating message:", error);
    }
  };

  const clearConversation = () => {
    setMessages([]);
    setBranchingOptions([]);
  };

  const exportConversation = () => {
    const conversationData = {
      character: character,
      messages: messages,
      timestamp: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(conversationData, null, 2)], {
      type: 'application/json'
    });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `conversation-${character.name}-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="enhanced-chatbox-container">
      <EnhancedHeader 
        character={character} 
        onBack={onBack}
        onSettings={() => setShowSettings(!showSettings)}
      />

      {showSettings && (
        <div className="settings-panel">
          <h3>Settings</h3>
          <div className="setting-group">
            <label>Dialogue Mode:</label>
            <select 
              value={dialogueMode} 
              onChange={(e) => setDialogueMode(e.target.value)}
            >
              <option value="freeform">Free Chat</option>
              <option value="branching">Branching</option>
            </select>
          </div>
          <div className="setting-actions">
            <button onClick={clearConversation} className="action-btn">
              🗑️ Clear Chat
            </button>
            <button onClick={exportConversation} className="action-btn">
              💾 Export
            </button>
          </div>
        </div>
      )}

      <div className="messages-container">
        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            message={message}
            character={character}
            onTranslate={translateMessage}
            onRegenerate={regenerateMessage}
          />
        ))}
        
        {isLoading && (
          <div className="typing-indicator">
            <div className="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span className="typing-text">
              {character?.name} is typing...
            </span>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <EnhancedChatInput
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
        dialogueMode={dialogueMode}
        branchingOptions={branchingOptions}
        onOptionSelect={handleOptionSelect}
        placeholder={
          dialogueMode === "branching" 
            ? "Select an option above or type your own response..." 
            : "Type your message..."
        }
      />
    </div>
  );
};

export default EnhancedChatBox;

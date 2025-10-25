import React, { useState, useEffect, useRef, useCallback } from "react";
import './ChatBox.css';

const ChatBox = ({ character, personality }) => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [dialogueMode, setDialogueMode] = useState("freeform"); // "freeform" or "branching"
  const [branchingOptions, setBranchingOptions] = useState([]);
  const [sessionId] = useState(() => Date.now().toString());
  const [characterId, setCharacterId] = useState(null);
  const [ws, setWs] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Create character profile when component mounts
    if (character && personality) {
      createCharacterProfile();
    }
  }, [character, personality, createCharacterProfile]);

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
      
      // Initialize conversation
      const welcomeMessage = {
        id: Date.now(),
        type: "npc",
        content: `Greetings! I'm ${character.name}, ${character.desc}. How can I assist you today?`,
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

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !characterId) return;

    const playerMessage = {
      id: Date.now(),
      type: "player",
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, playerMessage]);
    setIsLoading(true);

    if (dialogueMode === "freeform") {
      // Use WebSocket for real-time communication
      if (ws) {
        ws.send(JSON.stringify({ message: inputMessage }));
      } else {
        // Fallback to HTTP
        try {
          const response = await fetch("http://localhost:8000/api/dialogue/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              message: inputMessage,
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
      }
    } else {
      // Branching dialogue
      try {
        const response = await fetch("http://localhost:8000/api/dialogue/branching", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            character_id: characterId,
            session_id: sessionId,
            selected_option: inputMessage
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
    }

    setInputMessage("");
  };

  const handleOptionSelect = (option) => {
    setInputMessage(option);
    setBranchingOptions([]);
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
      
      // Update the message with translation
      setMessages(prev => prev.map(m => 
        m.id === messageId 
          ? { ...m, translation: data.translated, translatedLanguage: targetLanguage }
          : m
      ));
    } catch (error) {
      console.error("Error translating message:", error);
    }
  };

  return (
    <div className="chatbox-container">
      <div className="chatbox-header">
        <h2>🗣️ {character?.name} - Dialogue Generator</h2>
        <div className="mode-selector">
          <button 
            className={dialogueMode === "freeform" ? "active" : ""}
            onClick={() => setDialogueMode("freeform")}
          >
            Free Chat
          </button>
          <button 
            className={dialogueMode === "branching" ? "active" : ""}
            onClick={() => setDialogueMode("branching")}
          >
            Branching
          </button>
        </div>
      </div>

      <div className="messages-container">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.type}`}>
            <div className="message-content">
              <strong>{message.type === "player" ? "You" : character?.name}:</strong>
              <p>{message.content}</p>
              {message.translation && (
                <p className="translation">
                  <em>({message.translatedLanguage}): {message.translation}</em>
                </p>
              )}
              <div className="message-actions">
                <button 
                  onClick={() => translateMessage(message.id, "spanish")}
                  className="translate-btn"
                >
                  🇪🇸 Translate
                </button>
                <button 
                  onClick={() => translateMessage(message.id, "french")}
                  className="translate-btn"
                >
                  🇫🇷 Translate
                </button>
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message npc">
            <div className="message-content">
              <strong>{character?.name}:</strong>
              <p>💭 Thinking...</p>
            </div>
          </div>
        )}
        
        {branchingOptions.length > 0 && (
          <div className="branching-options">
            <h4>Choose your response:</h4>
            {branchingOptions.map((option, index) => (
              <button 
                key={index}
                className="option-button"
                onClick={() => handleOptionSelect(option)}
              >
                {option}
              </button>
            ))}
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
          placeholder={dialogueMode === "branching" ? "Select an option above or type your own response..." : "Type your message..."}
          disabled={isLoading}
        />
        <button 
          onClick={handleSendMessage}
          disabled={!inputMessage.trim() || isLoading}
          className="send-button"
        >
          {isLoading ? "⏳" : "🚀"}
        </button>
      </div>
    </div>
  );
};

export default ChatBox;

import React, { useState } from 'react';
import HomePage from './pages/HomePage.jsx';
import CharacterSelect from './pages/CharacterSelect.jsx';
import PersonalitySetup from './pages/PersonalitySetup.jsx';
import ChatBox from './pages/ChatBox.jsx';
import EnhancedChatBox from './pages/EnhancedChatBox.jsx';

const App = () => {
  const [stage, setStage] = useState('home'); // 'home' | 'character' | 'personality' | 'chatbox'
  const [selectedCharacter, setSelectedCharacter] = useState(null);
  const [personality, setPersonality] = useState('');

  const handleStart = () => setStage('character');

  const handleCharacterConfirm = (character) => {
    setSelectedCharacter(character);
    setStage('personality');
  };

  const handlePersonalityConfirm = (personalityText) => {
    setPersonality(personalityText);
    setStage('chatbox');
  };

  const handleBackToPersonality = () => {
    setStage('personality');
  };

  return (
    <>
      {stage === 'home' && <HomePage onStart={handleStart} />}
      {stage === 'character' && <CharacterSelect onConfirm={handleCharacterConfirm} />}
      {stage === 'personality' && (
        <PersonalitySetup
          selectedCharacter={selectedCharacter}
          onConfirm={handlePersonalityConfirm}
        />
      )}
      {stage === 'chatbox' && (
        <EnhancedChatBox
          character={selectedCharacter}
          personality={personality}
          onBack={handleBackToPersonality}
        />
      )}
    </>
  );
};

export default App;

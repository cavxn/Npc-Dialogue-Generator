// src/pages/CharacterSelect.jsx
import React, { useState } from 'react';
import './CharacterSelect.css';

const characters = [
  {
    id: 1,
    name: "Cyber Warrior",
    desc: "Brave defender of NeoCity",
    avatar: "/images/img1.avif",
    detail: "Wields a plasma blade. Trained in zero-latency combat. Keeps NeoCity safe from rogue AIs."
  },
  {
    id: 2,
    name: "Tech Wizard",
    desc: "Master of AI spells",
    avatar: "/images/img2.webp",
    detail: "Controls algorithmic spells. Can manipulate drones, firewalls, and predictive logic."
  },
  {
    id: 3,
    name: "Galactic Trader",
    desc: "Knows the cost of every planet",
    avatar: "/images/img3.webp",
    detail: "Deals in rare planetary resources. A cunning negotiator with allies in every system."
  },
  {
    id: 4,
    name: "Star Archer",
    desc: "Precision and power",
    avatar: "/images/img4.jpg",
    detail: "Can snipe enemies light-years away. Uses starlight-charged arrows and stealth tactics."
  },
  {
    id: 5,
    name: "Quantum Healer",
    desc: "Mender of fractured code",
    avatar: "/images/img5.avif",
    detail: "Specialist in reversing entropy. Repairs damaged code, minds, and bodies across timelines."
  },
  {
    id: 6,
    name: "Nebula Ninja",
    desc: "Strikes from the shadows",
    avatar: "/images/img6.avif",
    detail: "Expert in infiltration. Vanishes in a puff of cosmic dust. Leaves no trace but fear."
  }
];

const CharacterSelect = ({ onConfirm }) => {
  const [selectedId, setSelectedId] = useState(null);
  const selectedChar = characters.find(c => c.id === selectedId);

  return (
    <div className="character-select-wrapper">
      <video autoPlay muted loop className="bg-video">
        <source src="/video1.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      <div className="character-select">
        <h1>Select Your Character</h1>
        <div className="character-grid">
          {characters.map((char) => (
            <div
              key={char.id}
              className={`char-card ${selectedId === char.id ? 'selected' : ''}`}
              onClick={() => setSelectedId(char.id)}
            >
              <div className="avatar">
                <img src={char.avatar} alt={char.name} />
              </div>
              <h2>{char.name}</h2>
              <p>{char.desc}</p>
              <div className="details">{char.detail}</div>
            </div>
          ))}
        </div>

        {selectedChar && (
          <button className="confirm-button" onClick={() => onConfirm(selectedChar)}>
            Confirm {selectedChar.name}
          </button>
        )}
      </div>
    </div>
  );
};

export default CharacterSelect;

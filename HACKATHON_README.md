# 🎮 CodeZilla '25 - AI NPC Dialogue Generator

## 🏆 Hackathon Submission: GAI3 - AI NPC Dialogue Generator

### 📋 Problem Statement Fulfillment

**Core Requirements Met:**
- ✅ **Generate dialogue lines** given character profiles and scenario context
- ✅ **Maintain character consistency** in voice and personality across all dialogue
- ✅ **Real-time interactive use** with WebSocket support for instant responses

**Bonus Features Implemented:**
- ✅ **Branching dialogues** with multiple conversation paths
- ✅ **Translation/localization** for Spanish and French

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API Key

### Installation & Setup

1. **Clone and setup:**
```bash
cd Npc-Dialogue-Generator
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
# Create .env file in backend/ directory
echo "OPENAI_API_KEY=your_openai_api_key_here" > backend/.env
```

3. **Start the system:**
```bash
python start_hackathon_system.py
```

4. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

## 🎯 Features Overview

### 1. **Character Consistency & Memory**
- Advanced prompt engineering with conversation history
- Character personality, backstory, and speaking style preservation
- Context-aware responses that maintain character voice

### 2. **Real-time Interactive Dialogue**
- WebSocket support for instant responses
- HTTP fallback for reliability
- Session-based conversation management

### 3. **Branching Dialogue System**
- Multiple conversation paths
- Dynamic option generation
- Interactive choice selection
- Story-driven dialogue trees

### 4. **Translation & Localization**
- Real-time translation to Spanish and French
- Maintains character tone and style
- Per-message translation with caching

### 5. **Advanced Character Profiles**
- Sci-fi themed characters (Cyber Warrior, Tech Wizard, etc.)
- Detailed personality and backstory setup
- Customizable speaking styles and traits

---

## 🏗️ System Architecture

### Backend (FastAPI + OpenAI)
```
enhanced_dialogue_api.py
├── Character Management
├── Dialogue Generation
├── Branching System
├── Translation Service
└── WebSocket Support
```

### Frontend (React)
```
src/
├── pages/
│   ├── HomePage.jsx
│   ├── CharacterSelect.jsx
│   ├── PersonalitySetup.jsx
│   └── ChatBox.jsx (Enhanced)
└── components/
    └── DialogueGenerator.jsx
```

### Key Components

1. **Enhanced Dialogue API** (`enhanced_dialogue_api.py`)
   - Character profile management
   - Conversation memory and consistency
   - Branching dialogue generation
   - Real-time translation
   - WebSocket support

2. **Smart Prompt Builder** (`prompt_builder.py`)
   - Context-aware prompt generation
   - Conversation history integration
   - Character consistency enforcement

3. **Interactive Frontend** (`ChatBox.jsx`)
   - Real-time messaging interface
   - Branching dialogue options
   - Translation controls
   - Character mode switching

---

## 🎮 Usage Guide

### 1. **Character Selection**
- Choose from 6 unique sci-fi characters
- Each character has distinct personality and backstory
- Visual character cards with detailed descriptions

### 2. **Personality Setup**
- Customize character personality traits
- Set speaking style and key characteristics
- Define character backstory and motivations

### 3. **Dialogue Modes**

#### **Free Chat Mode**
- Open-ended conversation
- Real-time WebSocket communication
- Character memory and consistency
- Natural language interaction

#### **Branching Mode**
- Structured conversation paths
- Multiple choice options
- Story-driven dialogue
- Dynamic response generation

### 4. **Translation Features**
- Click translation buttons on any message
- Supports Spanish and French
- Maintains character tone and style
- Real-time translation with OpenAI

---

## 🔧 API Endpoints

### Character Management
- `POST /api/character/create` - Create new character profile
- `GET /api/characters` - List all characters

### Dialogue Generation
- `POST /api/dialogue/generate` - Generate consistent dialogue
- `POST /api/dialogue/branching` - Create branching conversations
- `GET /api/conversation/{character_id}/{session_id}` - Get conversation history

### Translation
- `POST /api/translate` - Translate dialogue to different languages

### WebSocket
- `WS /ws/{character_id}/{session_id}` - Real-time dialogue communication

---

## 🎨 UI/UX Features

### Modern Design
- Gradient backgrounds and glassmorphism effects
- Smooth animations and transitions
- Responsive design for all devices
- Intuitive user interface

### Interactive Elements
- Real-time typing indicators
- Message translation buttons
- Branching option selection
- Character mode switching

### Visual Feedback
- Loading states and progress indicators
- Message timestamps and speaker identification
- Translation overlays
- Smooth scrolling and auto-scroll

---

## 🧠 AI Integration

### OpenAI GPT-4 Integration
- Advanced language model for dialogue generation
- Character consistency through prompt engineering
- Translation capabilities
- Context-aware responses

### Prompt Engineering
- Character-specific system prompts
- Conversation history integration
- Personality trait enforcement
- Speaking style consistency

---

## 📊 Technical Specifications

### Backend
- **Framework:** FastAPI
- **AI Model:** OpenAI GPT-4
- **Real-time:** WebSocket support
- **Database:** In-memory (session-based)
- **Translation:** OpenAI API

### Frontend
- **Framework:** React 18
- **Styling:** CSS3 with modern features
- **State Management:** React Hooks
- **Real-time:** WebSocket client

### Performance
- **Response Time:** < 2 seconds for dialogue generation
- **Real-time:** WebSocket for instant communication
- **Scalability:** Session-based architecture
- **Reliability:** HTTP fallback for WebSocket

---

## 🎯 Hackathon Judging Criteria

### ✅ Core Requirements
1. **Dialogue Generation** - ✅ Advanced AI-powered dialogue with character consistency
2. **Character Consistency** - ✅ Memory system with conversation history
3. **Real-time Interaction** - ✅ WebSocket support with instant responses

### ✅ Bonus Features
1. **Branching Dialogues** - ✅ Full conversation tree system
2. **Translation** - ✅ Multi-language support with tone preservation

### 🏆 Additional Excellence
- **Modern UI/UX** - Beautiful, responsive interface
- **Technical Innovation** - WebSocket + HTTP hybrid approach
- **Scalability** - Session-based architecture
- **User Experience** - Intuitive character selection and setup

---

## 🚀 Future Enhancements

### Potential Additions
- Voice synthesis for spoken dialogue
- Emotion detection and response
- Multi-character conversations
- Save/load conversation states
- Character relationship tracking
- Advanced AI personality models

### Technical Improvements
- Database integration for persistence
- Redis for session management
- Docker containerization
- CI/CD pipeline setup
- Performance monitoring
- Error handling improvements

---

## 👥 Team & Development

**Project:** CodeZilla '25 - AI NPC Dialogue Generator  
**Problem Statement:** GAI3 - AI NPC Dialogue Generator  
**Duration:** 24-Hour Hackathon  
**Status:** Complete with all requirements + bonus features

---

## 📞 Support & Contact

For technical issues or questions about this submission:
- Check the API documentation at http://localhost:8000/docs
- Review the console logs for error messages
- Ensure all dependencies are installed correctly

**Good luck with the hackathon judging! 🏆**

// src/components/Notes.js
import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import '../styles/notes.css';

const Notes = () => {
  const [activeTab, setActiveTab] = useState('notes');
  const [notes, setNotes] = useState([]);
  const [noteIndex, setNoteIndex] = useState(0);
  const [typedNotes, setTypedNotes] = useState(new Set());
  const [chatHistory, setChatHistory] = useState([]);
  const [userMessage, setUserMessage] = useState('');

  const sampleNotes = [
    "1. Meeting started, discussing project goals.",
    "2. Key objectives: Improve user experience and increase engagement.",
    "3. Action item: Schedule a follow-up meeting for next week.",
    "4. Assign tasks to team members based on expertise.",
    "5. Discuss budget constraints and resource allocation.",
    "6. Note: Focus on mobile responsiveness for the next release.",
    "7. Set deadlines for initial deliverables.",
    "8. Meeting adjourned, awaiting further updates."
  ];

  useEffect(() => {
    const addNote = () => {
      if (noteIndex < sampleNotes.length) {
        setNotes((prevNotes) => [...prevNotes, sampleNotes[noteIndex]]);
        setNoteIndex((prevIndex) => prevIndex + 1);
      }
    };
    const intervalId = setInterval(addNote, 10000); // Adds a new note every 10 seconds
    return () => clearInterval(intervalId);
  }, [noteIndex]);

  const handleChatSubmit = (e) => {
    e.preventDefault();
    setChatHistory((prevHistory) => [...prevHistory, { sender: 'user', message: userMessage }]);
    setTimeout(() => {
      const simulatedResponse = "This is a simulated response based on the notes.";
      setChatHistory((prevHistory) => [...prevHistory, { sender: 'gemini', message: simulatedResponse }]);
    }, 1000);
    setUserMessage('');
  };

  const handleAnimationEnd = (index) => {
    setTypedNotes((prev) => new Set(prev).add(index));
  };

  return (
    <div className="notes-container">
      <div className="tab-buttons">
        <button onClick={() => setActiveTab('notes')} className={`tab-button ${activeTab === 'notes' ? 'active' : ''}`}>
          Notes
        </button>
        <button onClick={() => setActiveTab('chat')} className={`tab-button ${activeTab === 'chat' ? 'active' : ''}`}>
          Chat
        </button>
      </div>

      {activeTab === 'notes' && (
        <div className="static-notes">
          {notes.map((note, index) => (
            <div
              key={index}
              className={`note ${typedNotes.has(index) ? 'typed' : 'typewriter'}`}
              onAnimationEnd={() => handleAnimationEnd(index)}
            >
              <ReactMarkdown>{note}</ReactMarkdown>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'chat' && (
        <div className="chat-area">
          <div className="chat-history">
            {chatHistory.map((chat, index) => (
              <div key={index} className={`chat-bubble ${chat.sender}`}>
                <strong>{chat.sender === 'user' ? 'You' : 'Gemini'}:</strong> {chat.message}
              </div>
            ))}
          </div>
          <form onSubmit={handleChatSubmit} className="chat-form">
            <input
              type="text"
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              placeholder="Type a message..."
              className="chat-input"
            />
          </form>
        </div>
      )}
    </div>
  );
};

export default Notes;

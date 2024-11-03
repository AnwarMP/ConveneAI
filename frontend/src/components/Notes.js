// src/components/Notes.js
import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

const Notes = () => {
  const [activeTab, setActiveTab] = useState('notes');
  const [notes, setNotes] = useState([]);
  const [noteIndex, setNoteIndex] = useState(0);
  const [chatHistory, setChatHistory] = useState([]);
  const [userMessage, setUserMessage] = useState('');

  // Sample notes for testing
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

  // Simulate note updates every 10 seconds
  useEffect(() => {
    const addNote = () => {
      if (noteIndex < sampleNotes.length) {
        setNotes((prevNotes) => [...prevNotes, sampleNotes[noteIndex]]);
        setNoteIndex((prevIndex) => prevIndex + 1);
      }
    };

    const intervalId = setInterval(addNote, 10000);
    return () => clearInterval(intervalId);
  }, [noteIndex]);

  // Handle chat message submission with simulated response
  const handleChatSubmit = (e) => {
    e.preventDefault();

    setChatHistory((prevHistory) => [...prevHistory, { sender: 'user', message: userMessage }]);
    
    // Simulate a response with a delay
    setTimeout(() => {
      const simulatedResponse = "This is a simulated response based on the notes.";
      setChatHistory((prevHistory) => [...prevHistory, { sender: 'gemini', message: simulatedResponse }]);
    }, 1000);

    setUserMessage(''); // Clear the input
  };

  return (
    <div style={{ padding: '20px', height: '100%', overflowY: 'scroll' }}>
      {/* Tab Navigation */}
      <div style={{ display: 'flex', marginBottom: '10px' }}>
        <button onClick={() => setActiveTab('notes')} style={{ flex: 1, padding: '10px', background: activeTab === 'notes' ? '#ccc' : '#eee' }}>
          Notes
        </button>
        <button onClick={() => setActiveTab('chat')} style={{ flex: 1, padding: '10px', background: activeTab === 'chat' ? '#ccc' : '#eee' }}>
          Chat
        </button>
      </div>

      {/* Notes Tab */}
      {activeTab === 'notes' && (
        <div>
          <ReactMarkdown>{notes.join("\n\n")}</ReactMarkdown>
        </div>
      )}

      {/* Chat Tab */}
      {activeTab === 'chat' && (
        <div>
          <div style={{ maxHeight: '300px', overflowY: 'auto', border: '1px solid #ddd', padding: '10px', marginBottom: '10px' }}>
            {chatHistory.map((chat, index) => (
              <div key={index} style={{ textAlign: chat.sender === 'user' ? 'right' : 'left', margin: '5px 0' }}>
                <strong>{chat.sender === 'user' ? 'You' : 'Gemini'}:</strong> {chat.message}
              </div>
            ))}
          </div>
          <form onSubmit={handleChatSubmit}>
            <input
              type="text"
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              placeholder="Type a message..."
              style={{ width: '100%', padding: '10px' }}
            />
          </form>
        </div>
      )}
    </div>
  );
};

export default Notes;

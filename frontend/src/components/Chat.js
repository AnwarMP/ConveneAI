import React, { useState } from 'react';

const Chat = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [userMessage, setUserMessage] = useState('');

  const handleChatSubmit = (e) => {
    e.preventDefault();
    if (userMessage.trim()) {
      setChatHistory((prevHistory) => [...prevHistory, { sender: 'user', message: userMessage }]);
      setUserMessage('');

      // Simulate an AI response after a delay
      setTimeout(() => {
        const aiResponse = "AI Response based on transcript and notes.";
        setChatHistory((prevHistory) => [...prevHistory, { sender: 'ai', message: aiResponse }]);
      }, 1000);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-history">
        {chatHistory.map((chat, index) => (
          <div key={index} className={`chat-bubble ${chat.sender}`}>
            {chat.message}
          </div>
        ))}
      </div>
      <form onSubmit={handleChatSubmit} className="chat-form">
        <input
          type="text"
          value={userMessage}
          onChange={(e) => setUserMessage(e.target.value)}
          placeholder="Type your message..."
          className="chat-input"
        />
        <button type="submit" className="chat-send-button">Send</button>
      </form>
    </div>
  );
};

export default Chat;

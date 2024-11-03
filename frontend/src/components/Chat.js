import React, { useState } from 'react';

const Chat = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [userMessage, setUserMessage] = useState('');

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (userMessage.trim()) {
      setChatHistory((prevHistory) => [...prevHistory, { sender: 'user', message: userMessage }]);
      const response = await fetch("http://localhost:5000/chat-gemini", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
          chat_history: chatHistory.map(chat => chat.message).join("\n"),
        }),
      });
      const data = await response.json();
      if (data && data.status === "success") {
        setChatHistory((prevHistory) => [
          ...prevHistory,
          { sender: 'ai', message: data.results.response },
        ]);
      } else {
        console.error("Error:", data.error);
      }
      setUserMessage("");
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

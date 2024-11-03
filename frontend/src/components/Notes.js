// src/components/Notes.js
import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import '../styles/notes.css';

const Notes = ({ notes }) => {
  // Get the current date and time once as a placeholder title
  const [date, setDate] = useState('');

  useEffect(() => {
    const now = new Date();
    const formattedDate = now.toLocaleDateString();
    const formattedTime = now.toLocaleTimeString();
    setDate(`${formattedDate} ${formattedTime}`);
  }, []); // Empty dependency array to ensure it only runs once

  return (
    <div className="notes-container">
      <h2 className="notes-title">{`Meeting Notes - ${date}`}</h2>
      <div className="static-notes">
        {notes.map((note, index) => (
          <div key={index} className="note fade-in">
            <ReactMarkdown>{note}</ReactMarkdown>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Notes;

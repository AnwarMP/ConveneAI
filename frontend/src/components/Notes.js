import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { useNotes } from '../context/NotesContext';

const Notes = () => {
  const { latestNote } = useNotes();
  const [date, setDate] = useState('');

  // Set initial date
  useEffect(() => {
    const now = new Date();
    setDate(`${now.toLocaleDateString()} ${now.toLocaleTimeString()}`);
  }, []);

  return (
    <div className="notes-container">
      <h2 className="notes-title">{`Meeting Notes - ${date}`}</h2>
      <div className="notes-content">
        <div className="note">
          <ReactMarkdown>{latestNote}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
};

export default Notes;
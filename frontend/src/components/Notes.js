// src/components/Notes.js
import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import '../styles/notes.css';
import { useNotes } from '../context/NotesContext';

const Notes = () => {
  const { notes } = useNotes();
  const [typedNotes, setTypedNotes] = useState(new Set());

  useEffect(() => {
    console.log('Notes: Current notes count:', notes.length);
  }, [notes]);

  const handleAnimationEnd = (index) => {
    console.log('Notes: Animation ended for note:', index);
    setTypedNotes((prev) => new Set(prev).add(index));
  };

  console.log('Notes: Rendering with notes:', notes);

  return (
    <div className="notes-container">
      <div className="tab-buttons">
        <button className="tab-button active">Notes</button>
      </div>

      <div className="static-notes">
        {notes.map((note, index) => {
          console.log(`Notes: Rendering note ${index}:`, note.slice(0, 50) + '...');
          return (
            <div
              key={index}
              className={`note ${typedNotes.has(index) ? 'typed' : 'typewriter'}`}
              onAnimationEnd={() => handleAnimationEnd(index)}
            >
              <ReactMarkdown>{note}</ReactMarkdown>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Notes;
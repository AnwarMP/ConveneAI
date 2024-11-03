// src/context/NotesContext.js
import React, { createContext, useContext, useState, useCallback } from 'react';

const NotesContext = createContext();

export const NotesProvider = ({ children }) => {
  const [notes, setNotes] = useState([]);

  const addNote = useCallback((note) => {
    console.log('NotesContext: Adding new note:', note.slice(0, 50) + '...');
    setNotes((prevNotes) => {
      const newNotes = [...prevNotes, note];
      console.log('NotesContext: New notes count:', newNotes.length);
      return newNotes;
    });
  }, []);

  console.log('NotesContext: Current notes count:', notes.length);

  return (
    <NotesContext.Provider value={{ notes, addNote }}>
      {children}
    </NotesContext.Provider>
  );
};

export const useNotes = () => {
  const context = useContext(NotesContext);
  if (!context) {
    console.error('NotesContext: useNotes must be used within a NotesProvider');
    throw new Error('useNotes must be used within a NotesProvider');
  }
  return context;
};
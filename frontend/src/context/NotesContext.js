import React, { createContext, useContext, useState, useCallback } from 'react';

const NotesContext = createContext();

const logWithTimestamp = (message, data = null) => {
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] NotesContext: ${message}`;
  if (data) {
    console.log(logMessage, data);
  } else {
    console.log(logMessage);
  }
};

export const NotesProvider = ({ children }) => {
  const [notes, setNotes] = useState([]);
  const [latestNote, setLatestNote] = useState('');

  const addNote = useCallback((note) => {
    logWithTimestamp('Adding new note', {
      notePreview: note.substring(0, 50) + (note.length > 50 ? '...' : ''),
    });

    // Update both the notes array and latest note
    setNotes(prev => [...prev, note]);
    setLatestNote(note);
  }, []);

  const updateNote = useCallback((updatedNote) => {
    logWithTimestamp('Updating note', {
      notePreview: updatedNote.substring(0, 50) + (updatedNote.length > 50 ? '...' : '')
    });

    setNotes(prev => {
      const newNotes = [...prev];
      // Replace last note with updated one
      if (newNotes.length > 0) {
        newNotes[newNotes.length - 1] = updatedNote;
      } else {
        newNotes.push(updatedNote);
      }
      return newNotes;
    });
    
    // Update latest note to trigger rerender
    setLatestNote(updatedNote);
  }, []);

  const clearNotes = useCallback(() => {
    logWithTimestamp('Clearing all notes');
    setNotes([]);
    setLatestNote('');
  }, []);

  const contextValue = {
    notes,
    latestNote,
    addNote,
    updateNote,
    clearNotes,
  };

  return (
    <NotesContext.Provider value={contextValue}>
      {children}
    </NotesContext.Provider>
  );
};

export const useNotes = () => {
  const context = useContext(NotesContext);
  if (!context) {
    logWithTimestamp('Error: useNotes called outside of NotesProvider');
    throw new Error('useNotes must be used within a NotesProvider');
  }
  return context;
};

export default NotesProvider;
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
  const [animationKeys, setAnimationKeys] = useState([]);
  const updateCountRef = React.useRef(0);

  const addNote = useCallback((note) => {
    logWithTimestamp('Adding new note', {
      notePreview: note.substring(0, 50) + (note.length > 50 ? '...' : ''),
      currentNotesCount: notes.length
    });

    setNotes(prev => {
      const newNotes = [...prev, note];
      logWithTimestamp('Notes array updated', {
        previousCount: prev.length,
        newCount: newNotes.length
      });
      return newNotes;
    });

    setAnimationKeys(prev => {
      const newKeys = [...prev, Date.now()];
      logWithTimestamp('Animation keys updated', {
        keyCount: newKeys.length,
        latestKey: newKeys[newKeys.length - 1]
      });
      return newKeys;
    });
  }, [notes.length]);

  const updateNote = useCallback((updatedNote) => {
    updateCountRef.current += 1;
    logWithTimestamp(`Updating note (update #${updateCountRef.current})`, {
      notePreview: updatedNote.substring(0, 50) + (updatedNote.length > 50 ? '...' : '')
    });

    setNotes(prev => {
      if (prev.length === 0) {
        logWithTimestamp('No existing notes, adding as first note');
        return [updatedNote];
      }
      
      const previousNote = prev[prev.length - 1];
      const newNotes = [...prev];
      newNotes[newNotes.length - 1] = updatedNote;
      
      logWithTimestamp('Note update comparison', {
        previousLength: previousNote.length,
        newLength: updatedNote.length,
        changeInChars: updatedNote.length - previousNote.length
      });
      
      return newNotes;
    });

    setAnimationKeys(prev => {
      const newKeys = [...prev];
      const newKey = Date.now();
      newKeys[newKeys.length - 1] = newKey;
      logWithTimestamp('Animation key updated', {
        keyIndex: newKeys.length - 1,
        newKey: newKey
      });
      return newKeys;
    });
  }, []);

  const clearNotes = useCallback(() => {
    logWithTimestamp('Clearing all notes', {
      notesCleared: notes.length,
      animationKeysCleared: animationKeys.length
    });
    
    setNotes([]);
    setAnimationKeys([]);
    updateCountRef.current = 0;
  }, [notes.length, animationKeys.length]);

  // Log state changes
  React.useEffect(() => {
    logWithTimestamp('Notes state changed', {
      totalNotes: notes.length,
      totalAnimationKeys: animationKeys.length,
      totalUpdates: updateCountRef.current
    });
  }, [notes, animationKeys]);

  const contextValue = {
    notes,
    animationKeys,
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
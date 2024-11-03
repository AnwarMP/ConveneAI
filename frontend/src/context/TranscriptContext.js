// src/context/TranscriptContext.js
import React, { createContext, useContext, useState, useCallback } from 'react';

const TranscriptContext = createContext();

export function TranscriptProvider({ children }) {
  const [transcriptBuffer, setTranscriptBuffer] = useState([]);
  const [processedMessages, setProcessedMessages] = useState(new Set());

  const addMessage = useCallback((message) => {
    setTranscriptBuffer(prev => {
      // Only add message if it hasn't been processed
      if (!processedMessages.has(message.id)) {
        const newBuffer = [...prev, message];
        
        // Keep only the latest 10 messages
        const finalBuffer = newBuffer.slice(-10);
        
        // Mark message as processed
        setProcessedMessages(prevSet => new Set([...prevSet, message.id]));
        
        return finalBuffer;
      }
      return prev;
    });
  }, [processedMessages]);

  const clearBuffer = useCallback(() => {
    setTranscriptBuffer([]);
  }, []);

  const getFormattedTranscript = useCallback(() => {
    return transcriptBuffer
      .map(msg => `[${msg.timestamp}] ${msg.userName}: ${msg.text}`)
      .join('\n');
  }, [transcriptBuffer]);

  return (
    <TranscriptContext.Provider 
      value={{
        transcriptBuffer,
        addMessage,
        clearBuffer,
        getFormattedTranscript
      }}
    >
      {children}
    </TranscriptContext.Provider>
  );
}

export function useTranscript() {
  const context = useContext(TranscriptContext);
  if (!context) {
    throw new Error('useTranscript must be used within a TranscriptProvider');
  }
  return context;
}
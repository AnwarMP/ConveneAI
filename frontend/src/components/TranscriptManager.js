// src/components/TranscriptManager.js
import React, { useEffect, useState } from 'react';
import { useTranscript } from '../context/TranscriptContext';
import { useNotes } from '../context/NotesContext';

const TranscriptManager = () => {
  const { transcriptBuffer, getFormattedTranscript, clearBuffer } = useTranscript();
  const { addNote } = useNotes();
  const [existingSummary, setExistingSummary] = useState("");

  // Function to send transcript and existing summary to backend
  const processTranscript = async (transcript) => {
    try {
      console.log('TranscriptManager: Sending transcript and summary to backend:', { existingSummary, transcript });

      const response = await fetch('http://localhost:5000/analyze-transcript', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          transcript: transcript,
          existing_summary: existingSummary // Pass the current summary
        }),
      });

      const data = await response.json();
      console.log('TranscriptManager: Backend response:', data);

      if (data && data.results && data.results.summary) {
        setExistingSummary(data.results.summary); // Update summary
        addNote(data.results.summary); // Add new note to context
        console.log('TranscriptManager: Updated summary and added new note');
      }

      // Clear the buffer after processing
      clearBuffer();
      console.log('TranscriptManager: Cleared transcript buffer');
    } catch (error) {
      console.error('TranscriptManager: Error processing transcript:', error);
    }
  };

  // Watch transcript buffer
  useEffect(() => {
    if (transcriptBuffer.length >= 10) {
      const transcript = getFormattedTranscript();
      console.log('TranscriptManager: Buffer reached 10 messages:', transcript);
      processTranscript(transcript);
    }
  }, [transcriptBuffer, getFormattedTranscript, clearBuffer]);

  // This component doesn't render anything
  return null;
};

export default TranscriptManager;

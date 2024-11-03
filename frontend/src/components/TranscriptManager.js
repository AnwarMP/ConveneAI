import React, { useEffect } from 'react';
import { useTranscript } from '../context/TranscriptContext';

// This component handles transcript processing without affecting VideoCall
const TranscriptManager = () => {
  const { transcriptBuffer, getFormattedTranscript, clearBuffer } = useTranscript();

  // Function to send transcript to backend
  const processTranscript = async (transcript) => {
    try {
      console.log('Sending transcript to backend:', transcript);
      
      const response = await fetch('http://localhost:5000/analyze-transcript', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          transcript: transcript
        }),
      });

      const data = await response.json();
      console.log('Backend response:', data);
      
      // Clear the buffer after processing
      clearBuffer();
      
    } catch (error) {
      console.error('Error processing transcript:', error);
    }
  };

  // Watch transcript buffer
  useEffect(() => {
    if (transcriptBuffer.length >= 10) {
      const transcript = getFormattedTranscript();
      console.log('Buffer reached 10 messages:', transcript);
      processTranscript(transcript);
    }
  }, [transcriptBuffer, getFormattedTranscript, clearBuffer]);

  // This component doesn't render anything
  return null;
};

export default TranscriptManager;
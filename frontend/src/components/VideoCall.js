// src/components/VideoCall.js
import React, { useEffect, useRef, useState } from 'react';
import DailyIframe from '@daily-co/daily-js';
import { useNotes } from '../context/NotesContext';

const VideoCall = ({ url }) => {
  const videoContainerRef = useRef(null);
  const callFrameRef = useRef(null);
  const [transcriptBuffer, setTranscriptBuffer] = useState([]);
  const { addNote } = useNotes();

  useEffect(() => {
    console.log("VideoCall: Component mounting");
    if (!callFrameRef.current) {
      console.log("VideoCall: Creating DailyIframe instance");
      callFrameRef.current = DailyIframe.createFrame(videoContainerRef.current, {
        showLeaveButton: true,
        showFullscreenButton: true,
        iframeStyle: {
          width: '100%',
          height: '100%',
        },
      });

      const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvIjp0cnVlLCJkIjoiNmI2YWQzMzYtNjZhMS00NDk2LWI3NWItMTQ5YTk1NGE5ZjAwIiwiaWF0IjoxNzMwNjAyMTU2fQ.2LAsgzL82X1JfxvDOGiLsajaERRCGWkSjtKX3u66NLc';

      callFrameRef.current.join({ url, token }).then(() => {
        console.log("VideoCall: Joined call, starting transcription");
        callFrameRef.current.startTranscription();
        console.log("VideoCall: Transcription started");
      });

      callFrameRef.current.on('app-message', (message) => {
        console.log('VideoCall: Received app message:', message);
        setTranscriptBuffer((prevBuffer) => {
          const updatedBuffer = [...prevBuffer, message.data];
          console.log('VideoCall: Current buffer size:', updatedBuffer.length);
          
          if (updatedBuffer.length >= 10) {
            console.log('VideoCall: Buffer full (10 messages), processing transcript');
            const formattedTranscript = updatedBuffer
              .map((msg) => `[${msg.timestamp}] ${msg.user_name || ""}: ${msg.text}`)
              .join('\n');
            console.log('VideoCall: Formatted transcript:', formattedTranscript);
            sendTranscriptToBackend(formattedTranscript);
            return [];
          }
          return updatedBuffer;
        });
      });
    }

    return () => {
      console.log("VideoCall: Cleaning up");
      if (callFrameRef.current) {
        callFrameRef.current.leave();
        callFrameRef.current.destroy();
        callFrameRef.current = null;
      }
    };
  }, [url]);

  const sendTranscriptToBackend = async (transcript) => {
    try {
      console.log('VideoCall: Sending transcript to backend:', transcript);
      
      const response = await fetch('http://localhost:5000/analyze-transcript', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript }),
      });

      const data = await response.json();
      console.log('VideoCall: Received response from backend:', data);
      
      if (data && data.results && data.results.summary) {
        console.log('VideoCall: Adding new note to context:', data.results.summary);
        addNote(data.results.summary);
      }
    } catch (error) {
      console.error("VideoCall: Error sending transcript:", error);
    }
  };

  return <div ref={videoContainerRef} style={{ width: '100%', height: '100%' }} />;
};

export default VideoCall;
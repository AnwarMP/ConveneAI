import React, { useEffect, useRef, useState } from 'react';
import DailyIframe from '@daily-co/daily-js';
import { useNotes } from '../context/NotesContext';
import { useNavigate } from 'react-router-dom';

const VideoCall = ({ url }) => {
  const videoContainerRef = useRef(null);
  const callFrameRef = useRef(null);
  const [transcriptBuffer, setTranscriptBuffer] = useState([]);
  const { addNote } = useNotes();
  const currentSummaryRef = useRef('');
  const fullTranscriptRef = useRef('');
  const [meetingLeft, setMeetingLeft] = useState(false);
  const navigate = useNavigate();

  const logWithTimestamp = (message, data = null) => {
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] VideoCall: ${message}`;
    if (data) {
      console.log(logMessage, data);
    } else {
      console.log(logMessage);
    }
  };

  const sendTranscriptToBackend = async (newTranscript) => {
    try {
      logWithTimestamp('Sending transcript to backend:', {
        newSegmentLength: newTranscript.length,
        fullTranscriptLength: fullTranscriptRef.current.length
      });
      
      const response = await fetch('http://localhost:5000/analyze-transcript', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          transcript: newTranscript,
          existing_summary: currentSummaryRef.current,
          full_transcript: fullTranscriptRef.current 
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      logWithTimestamp('Received response from analysis:', data);
      
      if (data?.status === 'success' && data.results?.summary) {
        currentSummaryRef.current = data.results.summary;
        // Append new transcript to full history
        fullTranscriptRef.current = fullTranscriptRef.current 
          ? `${fullTranscriptRef.current}\n${newTranscript}`
          : newTranscript;

        // Save both raw transcript and current summary
        localStorage.setItem('raw_transcript', fullTranscriptRef.current);
        localStorage.setItem('meeting_summary', currentSummaryRef.current);
        localStorage.setItem('meeting_date', new Date().toISOString());
        
        logWithTimestamp('Adding new note to context:', data.results.summary);
        addNote(data.results.summary);
      } else {
        throw new Error('Invalid response format from server');
      }
    } catch (error) {
      logWithTimestamp('Error sending transcript:', error);
    }
  };

  useEffect(() => {
    logWithTimestamp('Component mounting');
    
    if (!callFrameRef.current) {
      logWithTimestamp('Creating DailyIframe instance');
      callFrameRef.current = DailyIframe.createFrame(videoContainerRef.current, {
        showLeaveButton: true,
        showFullscreenButton: true,
        iframeStyle: {
          width: '100%',
          height: '100%',
        },
      });

      const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvIjp0cnVlLCJkIjoiNmI2YWQzMzYtNjZhMS00NDk2LWI3NWItMTQ5YTk1NGE5ZjAwIiwiaWF0IjoxNzMwNjAyMTU2fQ.2LAsgzL82X1JfxvDOGiLsajaERRCGWkSjtKX3u66NLc';

      callFrameRef.current.join({ url, token })
        .then(() => {
          logWithTimestamp('Joined call, starting transcription');
          return callFrameRef.current.startTranscription();
        })
        .then(() => {
          logWithTimestamp('Transcription started');
        })
        .catch(error => {
          logWithTimestamp('Error setting up call:', error);
        });

      callFrameRef.current.on('app-message', (message) => {
        logWithTimestamp('Received app message:', message);
        setTranscriptBuffer((prevBuffer) => {
          const updatedBuffer = [...prevBuffer, message.data];
          logWithTimestamp('Current buffer size:', updatedBuffer.length);
          
          if (updatedBuffer.length >= 5) {
            logWithTimestamp('Buffer full (5 messages), processing transcript');
            const formattedTranscript = updatedBuffer
              .map((msg) => `[${msg.timestamp}] ${msg.user_name || ""}: ${msg.text}`)
              .join('\n');
            logWithTimestamp('Formatted transcript:', formattedTranscript);
            sendTranscriptToBackend(formattedTranscript);
            return [];
          }
          return updatedBuffer;
        });
      });

      callFrameRef.current.on('error', (error) => {
        logWithTimestamp('Daily.co error:', error);
      });

      callFrameRef.current.on('left-meeting', (event) => {
        logWithTimestamp('Left meeting:', event);
        setMeetingLeft(true);
      });
    }

    return () => {
      logWithTimestamp('Cleaning up');
      if (callFrameRef.current) {
        callFrameRef.current.leave();
        callFrameRef.current.destroy();
        callFrameRef.current = null;
      }
    };
  }, [url]);

  // Handle meeting end
  useEffect(() => {
    if (meetingLeft) {
      const finalizeMeeting = async () => {
        try {
          // // Process any remaining transcript
          // if (transcriptBuffer.length > 5) {
          //   logWithTimestamp('Processing final transcript buffer');
          //   const finalTranscript = transcriptBuffer
          //     .map((msg) => `[${msg.timestamp}] ${msg.user_name || ""}: ${msg.text}`)
          //     .join('\n');
          //   await sendTranscriptToBackend(finalTranscript);
          // }

          // Small delay to ensure storage is complete
          setTimeout(() => {
            logWithTimestamp('Navigating to summary page');
            navigate('/summary');
          }, 6000);
          
        } catch (error) {
          logWithTimestamp('Error in meeting finalization:', error);
          navigate('/summary'); // Navigate anyway
        }
      };

      finalizeMeeting();
    }
  }, [meetingLeft, transcriptBuffer, navigate]);

  return (    
    <>
      {meetingLeft ? (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
          <style>
            {`
              .loading-circle {
                margin: 10px auto;
                border: 16px solid #f3f3f3;
                border-top: 16px solid #3498db;
                border-radius: 50%;
                width: 120px;
                height: 120px;
                animation: spin 2s linear infinite;
              }
              @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
              }
            `}
          </style>
          <div className="loading-circle"></div>
          <p>Saving meeting transcript and moving to summary...</p>
        </div>
      ) : (
        <div ref={videoContainerRef} style={{ width: '100%', height: '100%' }} />
      )}
    </>
  );
};

export default VideoCall;
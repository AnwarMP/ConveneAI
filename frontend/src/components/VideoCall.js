// src/components/VideoCall.js
import React, { useEffect, useRef } from 'react';
import DailyIframe from '@daily-co/daily-js';

const VideoCall = ({ url }) => {
  const videoContainerRef = useRef(null);
  const callFrameRef = useRef(null);

  useEffect(() => {
    console.log("Mounting VideoCall component");

    if (!callFrameRef.current) {
      console.log("Creating DailyIframe instance with built-in controls");
      callFrameRef.current = DailyIframe.createFrame(videoContainerRef.current, {
        showLeaveButton: true,
        showFullscreenButton: true,
        iframeStyle: {
          width: '100%',
          height: '100%',
        },
      });

      // Meeting token to make you owner of meeting -> need to enable transcription
      const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvIjp0cnVlLCJkIjoiNmI2YWQzMzYtNjZhMS00NDk2LWI3NWItMTQ5YTk1NGE5ZjAwIiwiaWF0IjoxNzMwNjAyMTU2fQ.2LAsgzL82X1JfxvDOGiLsajaERRCGWkSjtKX3u66NLc';
      // Join the call without starting recording
      callFrameRef.current.join({ url, token }).then(() => {
        console.log("Joined the call");
        //Start transcription immediately when you join meeting
        callFrameRef.current.startTranscription();
        console.log("Started the transcript");
      });

      // Listen for recording events
      callFrameRef.current.on('recording-started', () => {
        console.log("Recording started");
      });

      callFrameRef.current.on('recording-stopped', (event) => {
        console.log("Recording stopped, recording info:", event);

        // Access the recording URL if available
        const recordingUrl = event?.recording?.download_url;
        if (recordingUrl) {
          console.log("Recording available at:", recordingUrl);
          // Optionally, handle the recording URL as needed
        }
      });

      // Add app-message event listener
      callFrameRef.current.on('app-message', (message) => {
        console.log("App message received:", message);
      });
    }

    return () => {
      if (callFrameRef.current) {
        console.log("Cleaning up DailyIframe instance");

        // Leave the call and clean up
        callFrameRef.current.leave();
        callFrameRef.current.destroy();
        callFrameRef.current = null;
      }
    };
  }, [url]);

  return <div ref={videoContainerRef} style={{ width: '100%', height: '100%' }} />;
};

export default VideoCall;

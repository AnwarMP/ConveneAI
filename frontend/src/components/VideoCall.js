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

      // Join the call without starting recording
      callFrameRef.current.join({ url }).then(() => {
        console.log("Joined the call");
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

// src/components/VideoCall.js
import React, { useEffect, useRef } from 'react';
import DailyIframe from '@daily-co/daily-js';

const VideoCall = ({ url }) => {
  const videoContainerRef = useRef(null);
  const callFrameRef = useRef(null);

  useEffect(() => {
    console.log("Mounting VideoCall component");

    if (!callFrameRef.current) {
      console.log("Creating DailyIframe instance");
      callFrameRef.current = DailyIframe.createFrame(videoContainerRef.current, {
        showLeaveButton: true,
        iframeStyle: {
          width: '100%',
          height: '100%',
        },
      });

      // Join the call and start recording
      callFrameRef.current.join({ url }).then(() => {
        console.log("Joined the call, starting recording...");
        callFrameRef.current.startRecording();
      });

      // Listen for recording events
      callFrameRef.current.on('recording-started', () => {
        console.log("Recording started");
      });

      callFrameRef.current.on('recording-stopped', (event) => {
        console.log("Recording stopped, recording info:", event);
        // Access the recording ID and URL from event data
        const recordingUrl = event?.recording?.download_url;
        if (recordingUrl) {
          console.log("Recording available at:", recordingUrl);
          // Optionally, you could trigger a download or save the URL
        }
      });
    }

    return () => {
      if (callFrameRef.current) {
        console.log("Cleaning up DailyIframe instance");

        // Stop recording when leaving the call
        callFrameRef.current.stopRecording().then(() => {
          console.log("Stopped recording before leaving the call");
        });

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

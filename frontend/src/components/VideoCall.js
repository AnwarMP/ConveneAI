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
      callFrameRef.current.join({ url });
    }

    return () => {
      if (callFrameRef.current) {
        console.log("Cleaning up DailyIframe instance");
        callFrameRef.current.leave();
        callFrameRef.current = null;
      }
    };
  }, [url]);

  return <div ref={videoContainerRef} style={{ width: '100%', height: '100%' }} />;
};

export default VideoCall;

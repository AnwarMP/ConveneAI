// src/pages/Meeting.js
import React, { useState, useEffect } from 'react';
import VideoCall from '../components/VideoCall';
import Notes from '../components/Notes';
import '../App.css';

export const Meeting = () => {
  const dailyUrl = 'https://conveneai.daily.co/conveneAI';
  const [notes, setNotes] = useState([]);

  useEffect(() => {
    // Example transcript segments for a simulated meeting
    const exampleTranscript = [
      "1. Meeting started: Introduction and welcome by the host.",
      "2. Objective: Discuss improvements for the user experience in the next product release.",
      "3. Action item: Set up a dedicated team for UX research.",
      "4. Deadline set for initial UX findings by the end of Q1.",
      "5. Budget constraints noted, focus on essential features only.",
      "6. Key point: Ensure mobile responsiveness in the redesign.",
      "7. Decision: Weekly team check-ins every Monday.",
      "8. Closing remarks: Next meeting scheduled for two weeks from today."
    ];

    // Simulate receiving each transcript segment in real-time
    const intervalId = setInterval(() => {
      if (exampleTranscript.length > 0) {
        const newSegment = exampleTranscript.shift(); // Get the next transcript segment
        setNotes((prevNotes) => [...prevNotes, newSegment]); // Add it to notes
      }
    }, 10000); // Update every 10 seconds

    return () => clearInterval(intervalId); // Cleanup on component unmount
  }, []);

  return (
    <div className="app-container">
      <div className="video-section">
        <VideoCall url={dailyUrl} />
      </div>
      <div className="notes-section">
        <Notes notes={notes} />
      </div>
    </div>
  );
};

export default Meeting;

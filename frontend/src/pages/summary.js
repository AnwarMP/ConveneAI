// src/pages/Summary.js
import React, { useState } from 'react';
import Nav from '../components/Nav';
import Chat from '../components/Chat'; // Import the Chat component
import '../styles/summary.css';

export const Summary = () => {
  const [isTranscriptExpanded, setTranscriptExpanded] = useState(false); // State to track transcript visibility

  const toggleTranscript = () => {
    setTranscriptExpanded(!isTranscriptExpanded);
  };

  return (
    <div>
      <Nav />
      <div className="summary-container">
        <div className="left-section">
          <div className="recording">
            <h2>Meeting Recording</h2>
            <div className="recording-placeholder">
              <video controls width="100%">
                <source src="placeholder-video.mp4" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          </div>

          <div className="transcript">
            <div className="transcript-header">
              <h2>Transcript</h2>
              <button className="transcript-toggle" onClick={toggleTranscript}>
                {isTranscriptExpanded ? "Collapse Transcript" : "Expand Transcript"}
              </button>
            </div>
            {isTranscriptExpanded && (
              <div className="transcript-content">
                <p>[00:00] Host: Welcome everyone to today's meeting...</p>
                <p>[00:05] Participant 1: Thank you for organizing this...</p>
                <p>[00:10] Participant 2: I think we should start by addressing...</p>
                {/* Add more transcript lines as necessary */}
              </div>
            )}
          </div>

          <div className="notes">
            <h2>Meeting Notes</h2>
            <div className="notes-content">
              <ul>
                <li>Meeting started: Introduction and welcome by the host.</li>
                <li>Objective: Discuss improvements for user experience in the next release.</li>
                <li>Action item: Assign tasks to UX and design teams.</li>
                <li>Decision: Weekly team check-ins every Monday.</li>
                <li>Next steps: Collect feedback from stakeholders.</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="right-section">
          <div className="chat-box-container">
            <h2>Chat with Gemini</h2>
            <Chat />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Summary;

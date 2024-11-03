// src/pages/Summary.js
import React from 'react';
import Nav from '../components/Nav';
import Chat from '../components/Chat'; // Import the Chat component
import '../styles/summary.css';

export const Summary = () => {
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

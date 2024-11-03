import React from 'react';
import Nav from '../components/Nav';
import Chat from '../components/Chat';
import '../styles/summary.css';
import TranscriptViewer from '../components/TranscriptViewer';
import { useNotes } from '../context/NotesContext';

export const Summary = () => {
  const { notes } = useNotes();

  return (
    <div>
      <Nav />
      <div className="summary-container">
        <div className="left-section">
          <div className="recording">
            <h2>Meeting Recording</h2>
            <div className="recording-placeholder">
              <video controls width="100%">
                <source src="/v2.mp4" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          </div>

          <div className="notes">
            <h2>Meeting Notes</h2>
            <div className="notes-content">
              <ul>
                {notes.map((note, index) => (
                  <li key={index}>{note}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div className="right-section">
          <div className="chat-box-container">
            <h2>Chat with Gemini</h2>
            <Chat />
          </div>
          <TranscriptViewer />
        </div>
      </div>
    </div>
  );
};

export default Summary;

// src/App.js
import React from 'react';
import VideoCall from './components/VideoCall';
import Notes from './components/Notes'; // Import the Notes component
import './App.css';

const App = () => {
  const dailyUrl = 'https://xuanwill.daily.co/eJkmkQn5KmAjUSg07HHa'; 
  return (
    <div className="app-container">
      <div className="video-section">
        <VideoCall url={dailyUrl} />
      </div>
      <div className="notes-section">
        <Notes /> {/* Add the Notes component */}
      </div>
    </div>
  );
};

export default App;

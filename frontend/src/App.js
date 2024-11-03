// src/App.js
import React from 'react';
import VideoCall from './components/VideoCall';
import './App.css';

const App = () => {
  const dailyUrl = 'https://conveneai.daily.co/conveneAI'; 
  return (
    <div className="app-container">
      <div className="video-section">
        <VideoCall url={dailyUrl} />
      </div>
      {/* Other components, e.g., Notes */}
    </div>
  );
};

export default App;

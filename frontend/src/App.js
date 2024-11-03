// src/App.js
import React from 'react';
import VideoCall from './components/VideoCall';
import './App.css';

const App = () => {
  const dailyUrl = 'https://xuanwill.daily.co/eJkmkQn5KmAjUSg07HHa'; 
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

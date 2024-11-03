// src/pages/Meeting.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import VideoCall from '../components/VideoCall';
import Notes from '../components/Notes';
import '../App.css';

export const Meeting = () => {
  const dailyUrl = 'https://conveneai.daily.co/conveneAI';

  return (
    <div className="app-container">
      <div className="video-section">
        <VideoCall url={dailyUrl} />
      </div>
      <div className="notes-section">
        <Notes />
      </div>
    </div>
  );
};

export default Meeting;

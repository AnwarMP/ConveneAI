// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Landing } from "./pages/landing";
import { Meeting } from "./pages/meeting";
import { Summary } from "./pages/summary";
import { NotesProvider } from './context/NotesContext';

import './App.css';

const App = () => {
  return (
    <NotesProvider>
    <Router>
      <Routes>
        <Route exact path="/" element={<Landing />} />
        <Route exact path="/meeting" element={<Meeting />} />
        <Route exact path="/summary" element={<Summary />} />
      </Routes>
    </Router>
    </NotesProvider>

  );
};

export default App;

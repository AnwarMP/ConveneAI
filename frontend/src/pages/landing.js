import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/landing.css';
import Nav from '../components/Nav';

export const Landing = () => {
  return (
    <div className="landing-container">
      <Nav />
      <div className="content-wrapper">
        <div className="hero-section">
          <h1 className="hero-title">Convene<span className = "gradient-text">AI</span> </h1>
          <p className="hero-subtitle">Transform your meetings with real-time insights and seamless collaboration.</p>
          <Link to="/meeting" className="cta-button">Get Started</Link>
        </div>

        <div className="features-section">
          <div className="feature-card">
            <h3>AI-Powered Insights</h3>
            <p>Get live insights and summaries of your meetings powered by our intelligent AI.</p>
          </div>
          <div className="feature-card">
            <h3>Real-Time Collaboration</h3>
            <p>Collaborate in real-time with embedded chat and shared notes during your meetings.</p>
          </div>
          <div className="feature-card">
            <h3>Seamless Integrations</h3>
            <p>Integrate with tools you already use to make meetings more productive.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Landing;

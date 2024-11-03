
import React from 'react';
import { Link } from 'react-router-dom';
import Nav from '../components/Nav';
import '../styles/summary.css';

export const Summary = () => {
  return (
    <div>
        <Nav></Nav>
        <div className="container">
            <div className="left-section">
                <div className="recording">

                </div>
                <div className="notes">

                </div>
            </div>
            <div className="chat">

            </div>
        </div>
    </div>
  );
}

export default Summary;
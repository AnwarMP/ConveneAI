// src/components/Nav.js
import React from 'react';
import { Link } from 'react-router-dom';
import './Nav.css';

export const Nav = () => {
    return (
      <div className="nav">
        <Link to='/' className="logo-link">
          <div className='logo'>Convene<span className="gradient-text">AI</span></div>
        </Link>
        <Link to='/meeting' className="logo-link">
            <div className="join">Join A Meeting</div>
        </Link>
      </div>
    );
}

export default Nav;

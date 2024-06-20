import React from 'react';
import { Link } from 'react-router-dom';
import logo from './Encryptodev_Logo.png';
import './homePage.css'; // Import your CSS file for HomePage styling

const HomePage = () => {
  return (
    <div className="home-page-container">
      <div className="home-page-content">
        <h1>Welcome to Encryptodevs</h1>
        <img src={logo} alt="Encryptodevs_Logo" className="logo-image" />
        <p>
          Please <Link to="/login">Login</Link> or <Link to="/signup">Sign Up</Link> to continue.
        </p>
      </div>
    </div>
  );
};

export default HomePage;

import React from 'react';
import { Link } from 'react-router-dom';
import logo from './Encryptodev_Logo.png';

const HomePage = () => {
  return (
      <div>
          <h1>Welcome to encryptodevs</h1>
          <img src={logo} alt="Encryptodevs_Logo" style={{width: '200px', height: 'auto'}}/>
          <p>Please <Link to="/login">Login</Link> or <Link to="/signup">Sign Up</Link> to continue.</p>

      </div>
  );
};
export default HomePage
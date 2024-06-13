import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div>
      <h1>Welcome to encryptodevs</h1>
      <p>Please <Link to="/login">Login</Link> or <Link to="/signup">Sign Up</Link> to continue.</p>
    </div>
  );
};
export default HomePage
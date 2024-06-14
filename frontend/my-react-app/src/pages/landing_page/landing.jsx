// src/pages/landing_page/landing.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Landing = () => {
  const [userStatus, setUserStatus] = useState(null);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/user-status`, { withCredentials: true })
      .then(response => {
        setUserStatus(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the user status!', error);
      });
  }, []);

  return (
    <div>
      <h1>Welcome to the Landing Page</h1>
      <p>Status of user: {userStatus ? userStatus.message : 'Not logged in'}</p>
    </div>
  );
};

export default Landing;

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Landing = () => {
  const [userStatus, setUserStatus] = useState('Loading...'); // Initial loading state
  const [userName, setUserName] = useState(null); // Initial username state
  const [userIsOnline, setUserIsOnline] = useState(false); // Initial online/offline state
  const navigate = useNavigate();

  useEffect(() => {
    fetchUserStatus();
  }, []);

  const fetchUserStatus = () => {
    axios.get(`${process.env.REACT_APP_API_URL}/user-status`, { withCredentials: true })
      .then(response => {
        const { username, status } = response.data;
        setUserStatus(status);
        setUserName(username);
        setUserIsOnline(status === 'Online');
      })
      .catch(error => {
        console.error('Error fetching user status:', error);
        setUserStatus('Offline');
      });
  };

  const handleLogout = () => {
    axios.get(`${process.env.REACT_APP_API_URL}/logout`, { withCredentials: true })
      .then(response => {
        console.log(response.data.message);
        navigate('/');
      })
      .catch(error => {
        console.error('Error logging out:', error);
      });
  };

  return (
    <div>
      <h1>Welcome to encryptodevs</h1>
      {userName && (
        <p>Welcome, {userName} ({userIsOnline ? 'Online' : 'Offline'})</p>
      )}
      {!userName && (
        <p>Status of user: {userStatus}</p>
      )}
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Landing;

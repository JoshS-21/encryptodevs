import React, { useEffect, useState } from 'react';
import axios from 'axios';
// If using React Router for navigation
// import { useHistory } from 'react-router-dom';

const Landing = () => {
  const [userData, setUserData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  // If using React Router for navigation
  // const history = useHistory();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('No token available');
        }

        const response = await axios.get(`${process.env.REACT_APP_API_URL}/user-status`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        setUserData(response.data);
      } catch (error) {
        console.error('Error fetching user data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUserData();

  }, []);

  const handleLogout = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No token available');
      }

      await axios.get(`${process.env.REACT_APP_API_URL}/logout`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      localStorage.removeItem('token');
      // If using React Router for navigation
      // history.push('/login');  // Redirect to login page after logout
      // You can also use window.location.href = '/login'; for redirection

      // For now, just reload the page to simulate logout
      window.location.reload();
    } catch (error) {
      console.error('Error logging out:', error);
      // Handle error
    }
  };

  if (isLoading) {
    return <p>Loading user data...</p>;
  }

  return (
    <div>
      <h2>Welcome to the Landing Page</h2>
      {userData ? (
        <div>
          <p>Logged in as: {userData.username}</p>
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <p>No user data available</p>
      )}
    </div>
  );
};

export default Landing;

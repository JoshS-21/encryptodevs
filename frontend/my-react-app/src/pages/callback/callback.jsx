import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

const Callback = () => {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const token = params.get('token');

    if (token) {
      axios.post(`${process.env.REACT_APP_API_URL}/verify-google-token`, { token })
        .then(response => {
          if (response.status === 200) {
            localStorage.setItem('token', response.data.token);
            navigate('/landing');
          } else {
            console.error('Google Sign-In failed.');
          }
        })
        .catch(error => {
          console.error('Error verifying Google token:', error);
        });
    }
  }, [location, navigate]);

  return (
    <div>
      <h2>Processing Google Sign-In...</h2>
    </div>
  );
};

export default Callback;

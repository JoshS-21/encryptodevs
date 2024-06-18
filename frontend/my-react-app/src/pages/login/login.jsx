import React, { useState } from 'react';
import axios from 'axios';
import logo from './Encryptodev_Logo.png';


const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [errorMessage, setErrorMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData, // Spread the current formData to maintain existing state
      [e.target.name]: e.target.value // Update the specific field
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post(`${process.env.REACT_APP_API_URL}/login`, formData)
      .then(response => {
        alert(response.data.message);
        localStorage.setItem('token', response.data.token);
        window.location.href = '/landing';
      })
      .catch(error => {
        if (error.response && error.response.status === 401) {
          setErrorMessage('Username not found. Please sign up to create an account.');
        } else {
          console.error('Error logging in:', error);
          setErrorMessage('Login failed. Please try again.');
        }
      });
  };

  return (
      <div>
          <h2>Login</h2>
          <img src={logo} alt="Encryptodevs_Logo" style={{width: '200px', height: 'auto'}}/>
          <form onSubmit={handleSubmit}>
              <input
                  type="text"
                  name="username"
                  placeholder="Username"
                  value={formData.username}
                  onChange={handleChange}
                  autoComplete="username"
                  required
              />
              <br/>
              <input
                  type="password"
                  name="password"
                  placeholder="Password"
                  value={formData.password}
                  onChange={handleChange}
                  autoComplete="current-password"
                  required
              />
              <br/>
              <button type="submit">Login</button>
          </form>
          {errorMessage && <p style={{color: 'red'}}>{errorMessage}</p>}
          <p>Haven't got an account? <a href="/signup">Sign up</a></p>
          <p>Return to <a href="/">homepage</a></p>
      </div>
  );
};

export default Login;

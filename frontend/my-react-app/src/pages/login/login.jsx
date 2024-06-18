import React, { useState } from 'react';
import { Link } from 'react-router-dom';  // Import Link from react-router-dom
import axios from 'axios';

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [errorMessage, setErrorMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
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
        <br />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          autoComplete="current-password"
          required
        />
        <br />
        <button type="submit">Login</button>
      </form>
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      <br />
      <Link to="/forgot_password">Forgot Password?</Link>  
    </div>
  );
};

export default Login;

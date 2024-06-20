import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import logo from './Encryptodev_Logo.png';
import './login.css'; // Import your CSS file

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
          if (error.response.data.message === 'Incorrect password') {
            setErrorMessage('Incorrect password. Please try again.');
          } else {
            setErrorMessage('Username not found. Please sign up to create an account.');
          }
        } else {
          console.error('Error logging in:', error);
          setErrorMessage('Login failed. Please try again.');
        }
      });
  };

  return (
    <div className="page-container">
      <div className="top-left">
        <div className="logo-container">
          <img src={logo} alt="Encryptodevs_Logo" />
        </div>
      </div>
      <div className="top-right">
        <p>Need an account? <Link to="/signup">Sign up</Link></p>
      </div>
      <div className="login-container">
        <h2 id={"title"}>Login</h2>
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <input
              type="text"
              name="username"
              id={"username"}
              placeholder="Username"
              value={formData.username}
              onChange={handleChange}
              autoComplete="username"
              className="login-input"
              required
            />
          </div>
          <div className="form-group">
            <input
              type="password"
              name="password"
              id={"password"}
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              autoComplete="current-password"
              className="login-input"
              required
            />
          </div>
          <div className="form-group">
            <button type="submit" id={"submit"} className="login-input">Login</button>
          </div>
        </form>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        <br />
        <Link to="/forgot_password">Forgot Password?</Link>
      </div>
    </div>
  );
};

export default Login;

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [errorMessage, setErrorMessage] = useState('');
  const [profile, setProfile] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        if (response.status === 401) {
          setErrorMessage('Username not found. Please sign up to create an account.');
        } else {
          console.error('Error logging in:', errorData);
          setErrorMessage('Login failed. Please try again.');
        }
        return;
      }

      const data = await response.json();
      alert(data.message);
      localStorage.setItem('token', data.token);
      navigate('/landing');
    } catch (error) {
      console.error('Error logging in:', error);
      setErrorMessage('Login failed. Please try again.');
    }
  };

  const handleLoginSuccess =  async (credentialResponse)  => {
    const { profileObj, tokenId } = credentialResponse;
    const GoogleStatusResponse = await fetch(`${process.env.REACT_APP_API_URL}/verify-google-token`,{
            method: 'POST',
            headers: {
            Authorization: `Bearer ${credentialResponse.credential}`,
          }
        });
    console.log(GoogleStatusResponse)
    setProfile(profileObj);
    localStorage.setItem('token', credentialResponse.credential);
    console.log(tokenId)
    navigate('/landing');
  };

  const handleLoginFailure = (error) => {
    console.log('Google Login Failed:', error);
    setErrorMessage('Google Sign-In failed. Please try again.');
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
      <br />
      <Link to="/forgot_password">Forgot Password?</Link>
      <br />
      <h3>Or Login with Google:</h3>
      {profile ? (
        <div>
          <p>User ID: {profile.googleId}</p>
          <p>Email: {profile.email}</p>
        </div>
      ) : (
        <GoogleLogin
          onSuccess={handleLoginSuccess}
          onFailure={handleLoginFailure}
        />
      )}
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
    </div>
  );
};

export default Login;

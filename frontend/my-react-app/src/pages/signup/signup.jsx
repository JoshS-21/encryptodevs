import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import logo from "../landing_page/Encryptodev_Logo.png";

const Signup = () => {
  const [formData, setFormData] = useState({
    name: '',
    username: '',
    email: '',
    password: '',
    phone_number: ''
  });

  const [validationErrors, setValidationErrors] = useState({
    password: '',
    username: '',
    email: '',
    phone_number: ''
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });

    // Clear validation error for the changed field
    setValidationErrors({
      ...validationErrors,
      [name]: ''
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validate phone number length
    if (!/^\d{11}$/.test(formData.phone_number)) {
      setValidationErrors({ ...validationErrors, phone_number: 'Phone number must be exactly 11 digits' });
      return;
    } else {
      setValidationErrors({ ...validationErrors, phone_number: '' });
    }

    // Validate password requirements
    if (!/^.*(?=.{7,})(?=.*[!@£_%-])(?=.*[A-Z]).*$/.test(formData.password)) {
      setValidationErrors({
        ...validationErrors,
        password: 'Password must be at least 7 characters long, include at least one uppercase letter, and contain !@£_%- characters'
      });
      return;
    } else {
      setValidationErrors({ ...validationErrors, password: '' });
    }

    // Send signup request to backend
    axios.post(`${process.env.REACT_APP_API_URL}/signup`, formData)
      .then(response => {
        alert(response.data.message);
        setFormData({
          name: '',
          username: '',
          email: '',
          password: '',
          phone_number: ''
        });
        navigate('/login'); // Redirect after successful signup
      })
      .catch(error => {
        if (error.response && error.response.data && error.response.data.message) {
          const { message } = error.response.data;
          // Update validation errors based on server response
          if (message.includes('Username')) {
            setValidationErrors({ ...validationErrors, username: 'Username already exists' });
          } else if (message.includes('Email')) {
            setValidationErrors({ ...validationErrors, email: 'Email already exists' });
          } else if (message.includes('Phone number')) {
            setValidationErrors({ ...validationErrors, phone_number: 'Phone number already exists' });
          }
        } else {
          console.error('Error signing up:', error);
          alert('Signup failed. Please try again.');
        }
      });
  };

  return (
      <div>
        <h2>Signup</h2>
        <img src={logo} alt="Encryptodevs_Logo" style={{width: '200px', height: 'auto'}}/>
        <form onSubmit={handleSubmit}>
          <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} required/>
          <br/>
          <input type="text" name="username" placeholder="Username" value={formData.username} onChange={handleChange}
                 required/>
          {validationErrors.username && <p style={{color: 'red'}}>{validationErrors.username}</p>}
          <br/>
          <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required/>
          {validationErrors.email && <p style={{color: 'red'}}>{validationErrors.email}</p>}
          <br/>
          <input type="password" name="password" placeholder="Password" value={formData.password}
                 onChange={handleChange} required/>
          {validationErrors.password && <p style={{color: 'red'}}>{validationErrors.password}</p>}
          <br/>
          <input type="text" name="phone_number" placeholder="Phone Number" value={formData.phone_number}
                 onChange={handleChange} required/>
          {validationErrors.phone_number && <p style={{color: 'red'}}>{validationErrors.phone_number}</p>}
          <br/>
          <button type="submit">Signup</button>
          <p> Already have an account? <a href="/login">Sign in</a></p>
          <p>Return to <a href="/">homepage</a></p>

        </form>
      </div>
  );
};

export default Signup;


import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import './signup.css';

import logo from "../landing_page/Encryptodev_Logo.png";


const Signup = () => {
  const [formData, setFormData] = useState({
    name: '',
    username: '',
    email: '',
    password: '',
    phone_number: ''
  });

  const [passwordCriteria, setPasswordCriteria] = useState({
    length: false,
    uppercase: false,
    specialChar: false
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

    // Validate password requirements as user types
    if (name === 'password') {
      validatePassword(value);
    }
  };

  const validatePassword = (password) => {
    setPasswordCriteria({
      length: password.length >= 7,
      uppercase: /[A-Z]/.test(password),
      specialChar: /[!@£_%-]/.test(password)
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

    // If any password criteria is not met, do not proceed
    if (!passwordCriteria.length || !passwordCriteria.uppercase || !passwordCriteria.specialChar) {
      setValidationErrors({
        ...validationErrors,
        password: 'Password must meet all requirements'
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

    <div className="signup-container">
      <h2>Signup</h2>
       <img src={logo} alt="Encryptodevs_Logo" style={{width: '200px', height: 'auto'}}/>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <input type="text" name="username" placeholder="Username" value={formData.username} onChange={handleChange} required />
          {validationErrors.username && <p className="error-message">{validationErrors.username}</p>}
        </div>
        <div className="form-group">
          <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
          {validationErrors.email && <p className="error-message">{validationErrors.email}</p>}
        </div>
        <div className="form-group">
          <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required />
          {validationErrors.password && <p className="error-message">{validationErrors.password}</p>}
          <ul className="password-criteria">
            <li className={passwordCriteria.length ? 'met' : 'unmet'}>
              {passwordCriteria.length && <span className="checkmark">✔</span>} Password must be at least 7 characters long
            </li>
            <li className={passwordCriteria.uppercase ? 'met' : 'unmet'}>
              {passwordCriteria.uppercase && <span className="checkmark">✔</span>} Password must include at least one uppercase letter
            </li>
            <li className={passwordCriteria.specialChar ? 'met' : 'unmet'}>
              {passwordCriteria.specialChar && <span className="checkmark">✔</span>} Password must include at least one of !@£_%- characters
            </li>
          </ul>
        </div>
        <div className="form-group">
          <input type="text" name="phone_number" placeholder="Phone Number" value={formData.phone_number} onChange={handleChange} required />
          {validationErrors.phone_number && <p className="error-message">{validationErrors.phone_number}</p>}
        </div>
        <div className="form-group">
          <button type="submit">Signup</button>
        </div>
      </form>
    </div>

  );
};

export default Signup;

import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './ResetPassword.css'; // Assuming you have a separate CSS file

const ResetPassword = () => {
  const { token } = useParams();
  const [newPassword, setNewPassword] = useState('');
  const [message, setMessage] = useState('');
  const [passwordCriteria, setPasswordCriteria] = useState({
    length: false,
    uppercase: false,
    specialChar: false,
  });

  const validatePassword = (password) => {
    const criteria = {
      length: password.length >= 7,
      uppercase: /[A-Z]/.test(password),
      specialChar: /[!@£_%-]/.test(password),
    };
    setPasswordCriteria(criteria);
    return criteria.length && criteria.uppercase && criteria.specialChar;
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    if (!validatePassword(newPassword)) {
      setMessage('Password does not meet the criteria.');
      return;
    }
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/reset_password`, {
        reset_token: token,
        new_password: newPassword,
      });
      setMessage(response.data.message);
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.message);
      } else {
        setMessage('An error occurred. Please try again later.');
      }
    }
  };

  return (
    <div className="reset-container">
      <h2>Reset Password</h2>
      <form onSubmit={handleResetPassword}>
        <div className="form-group">
          <input
            type="password"
            placeholder="Enter new password"
            value={newPassword}
            onChange={(e) => {
              setNewPassword(e.target.value);
              validatePassword(e.target.value);
            }}
            required
          />
        </div>
        <ul className="password-criteria">
          <li className={passwordCriteria.length ? 'met' : 'unmet'}>
            <span className="checkmark">{passwordCriteria.length ? '✔️' : '❌'}</span>
            At least 7 characters
          </li>
          <li className={passwordCriteria.uppercase ? 'met' : 'unmet'}>
            <span className="checkmark">{passwordCriteria.uppercase ? '✔️' : '❌'}</span>
            At least one uppercase letter
          </li>
          <li className={passwordCriteria.specialChar ? 'met' : 'unmet'}>
            <span className="checkmark">{passwordCriteria.specialChar ? '✔️' : '❌'}</span>
            At least one special character (!@£_%-)
          </li>
        </ul>
        <button type="submit">Reset Password</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default ResetPassword;

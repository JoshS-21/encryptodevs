import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircle } from '@fortawesome/free-solid-svg-icons';

const Landing = () => {
  const [userData, setUserData] = useState(null);
  const [users, setUsers] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }

      const headers = { headers: { Authorization: `Bearer ${token}` } };
      const userResponse = await axios.get(`${process.env.REACT_APP_API_URL}/user-status`, headers);
      const usersResponse = await axios.get(`${process.env.REACT_APP_API_URL}/users`, headers);

      if (userResponse.status === 200) {
        setUserData(userResponse.data);
      } else {
        console.error('Failed to fetch user data');
        navigate('/login');
      }

      if (usersResponse.status === 200) {
        setUsers(usersResponse.data);
      } else {
        console.error('Failed to fetch users data');
        navigate('/login');
      }
    };

    fetchUserData();
  }, [navigate]);

  const handleLogout = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    const headers = { headers: { Authorization: `Bearer ${token}` } };
    const logoutResponse = await axios.post(`${process.env.REACT_APP_API_URL}/logout`, {}, headers);

    if (logoutResponse.status === 200) {
      localStorage.removeItem('token');
      setUserData(null);
      setUsers(users.map(user => ({
        ...user,
        is_online: user.user_id === userData?.user_id ? false : user.is_online
      })));

      navigate('/login');
    } else {
      console.error('Logout failed');
    }
  };

  return (
    <div>
      <h2>Welcome to the Landing Page</h2>
      {userData ? (
        <div>
          <p>Logged in as: {userData.username}</p>
          <p>
            Status:
            <FontAwesomeIcon
              icon={faCircle}
              style={{ color: userData.is_online ? 'green' : 'red', marginLeft: '8px' }}
            />
            {userData.is_online ? 'Online' : 'Offline'}
          </p>
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <p>User data is not available</p>
      )}
      <h3>All Users:</h3>
      <ul>
        {users.map(user => (
          <li key={user.user_id}>
            {user.username} -
            <FontAwesomeIcon
              icon={faCircle}
              style={{ color: user.is_online ? 'green' : 'red', marginLeft: '8px' }}
            />
            {user.is_online ? 'Online' : 'Offline'}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Landing;

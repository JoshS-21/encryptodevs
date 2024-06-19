import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircle } from '@fortawesome/free-solid-svg-icons';
import logo from './Encryptodev_Logo.png';

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

      try {
        // Fetch user status
        const userStatusResponse = await fetch(`${process.env.REACT_APP_API_URL}/user-status`, {
          headers: {
            Authorization: `Bearer ${token}`,
          }
        });

        if (!userStatusResponse.ok) {
          console.error("Failed to fetch user status");
          navigate('/login');
          return;
        }

        const userData = await userStatusResponse.json();
        setUserData(userData);

        // Fetch all users
        const usersResponse = await fetch(`${process.env.REACT_APP_API_URL}/users`, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (!usersResponse.ok) {
          console.error("Failed to fetch users data");
          navigate('/login');
          return;
        }

        const usersData = await usersResponse.json();
        setUsers(usersData);
      } catch (error) {
        console.error('Error fetching data:', error);
        navigate('/login');
      }
    };

    fetchUserData();
  }, [navigate]);

  const handleLogout = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const logoutResponse = await fetch(`${process.env.REACT_APP_API_URL}/logout`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (logoutResponse.ok) {
        localStorage.removeItem('token');
        setUserData(null);
        setUsers(users.map(user => ({
          ...user,
          is_online: user.user_id === userData?.user_id ? false : user.is_online,
          last_seen: user.user_id === userData?.user_id ? new Date().toISOString() : user.last_seen,
        })));

        navigate('/');
      } else {
        console.error('Logout failed');
      }
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const formatLastSeen = (lastSeen) => {
    if (!lastSeen || lastSeen === 'N/A') return 'N/A';
    const lastSeenDate = new Date(lastSeen);
    const now = new Date();
    const diffInMinutes = Math.floor((now - lastSeenDate) / 60000);

    if (diffInMinutes < 1) return 'just now';
    if (diffInMinutes < 60) return `${diffInMinutes} minutes ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)} hours ago`;

    return `on ${lastSeenDate.toLocaleDateString()} at ${lastSeenDate.toLocaleTimeString()}`;
  };

  return (
    <div>
      <h2>Welcome to the Landing Page</h2>
      <img src={logo} alt="Encryptodevs_Logo" style={{ width: '200px', height: 'auto' }} />
      {userData ? (
        <div>
          <p>Logged in as: {userData.username}</p>
          <p>
            Status:
            <FontAwesomeIcon
              icon={faCircle}
              style={{ color: userData.is_online ? 'green' : 'red', marginLeft: '8px' }}
            />
            {userData.is_online ? 'Online' : `Offline (Last seen: ${formatLastSeen(userData.last_seen)})`}
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
            {user.is_online ? 'Online' : `Offline (Last seen: ${formatLastSeen(user.last_seen)})`}
          </li>
        ))}
      </ul>
      <a href="/test">Messages</a>
    </div>
  );
};

export default Landing;

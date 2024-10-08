import React, {useEffect, useState} from 'react';
import axios from 'axios';
import {useNavigate} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'; //Styling package
import {faCircle} from '@fortawesome/free-solid-svg-icons'; //Styling for icon status
import logo from './Encryptodev_Logo.png';
import DropdownMenu from "../../components/dropdown";
import initializeWebSocket from "../../components/WebSocket.js";
import './landing.css'; // Import your CSS file


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

            const headers = {headers: {Authorization: `Bearer ${token}`}};
            const userResponse = await axios.get(`${process.env.REACT_APP_API_URL}/user-status`, headers);
            const usersResponse = await axios.get(`${process.env.REACT_APP_API_URL}/users`, headers);

            if (userResponse.status === 200) {
                setUserData(userResponse.data);
                console.log(userData);
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

        // Initialize WebSocket connection
        const socket = initializeWebSocket();

        // Clean up the WebSocket connection when the component unmounts
        return () => {
            if (socket) {
                socket.disconnect();
            }
        };
    }, [navigate]);

            console.log(users);

    const handleLogout = async () => {
        const token = localStorage.getItem('token');
        if (!token) return;

        const headers = {headers: {Authorization: `Bearer ${token}`}};
        const logoutResponse = await axios.post(`${process.env.REACT_APP_API_URL}/logout`,
            {}, headers);


        if (logoutResponse.status === 200) {
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
        <div className="page-container">
            <div className="logo-container">
                <img src={logo} alt="Encryptodevs_Logo" />
            </div>
            {userData ? (
                <div className="user-info-container">
                    <p id={"current_user"}>Logged in as: {userData.username}</p>
                    <div className="status-indicator">
                        Status:
                        <FontAwesomeIcon
                            icon={faCircle}
                            style={{ color: userData.is_online ? 'green' : 'red', marginLeft: '8px' }}
                        />
                        <span>{userData.is_online ? 'Online' : `Offline (Last seen: ${formatLastSeen(userData.last_seen)})`}</span>
                    </div>
                    <button className="logout-button" onClick={handleLogout}>Logout</button>
                </div>
            ) : (
                <p>User data is not available</p>
            )}

            <div className="users-list">
                <h3>All Users:</h3>
                <ul>
                    {users.map(user => (
                        <li key={user.user_id}>
                            {user.username}
                            <span>
                                <FontAwesomeIcon
                                    icon={faCircle}
                                    style={{ color: user.is_online ? 'green' : 'red', marginLeft: '8px' }}
                                />
                                {user.is_online ? 'Online' : `Offline (Last seen: ${formatLastSeen(user.last_seen)})`}
                            </span>
                        </li>
                    ))}
                </ul>
                <br/>
            </div>
                <DropdownMenu userData={userData} users={users} />
        </div>
    );
};

export default Landing;

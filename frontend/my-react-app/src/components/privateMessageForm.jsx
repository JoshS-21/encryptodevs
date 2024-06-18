import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import logo from './Encryptodev_Logo.png';


const PrivateMessageForm = () => {
  const [recipient, setRecipient] = useState('');
  const [message, setMessage] = useState('');
  const [sender, setSender] = useState('');
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('No token found, redirecting to login.');
      window.location.href = '/login'; // Redirect to login if no token is found
      return;
    }

    const serverUrl = 'http://localhost:5000'; // Replace with your server URL and port
    const newSocket = io(serverUrl, {
      query: { token: token },
    });
    setSocket(newSocket);

    newSocket.on('connect', () => {
      console.log('Socket connected with ID:', newSocket.id);
      newSocket.emit('connected', { socket_id: newSocket.id });
    });

    newSocket.on('new_private_message', (msg) => {
      alert(msg);
    });

    return () => {
      newSocket.disconnect();
    };
  }, []);

  const handleSendPrivateMessage = () => {
    if (socket) {
      socket.emit('private_message', { recipient, message, sender });
      setRecipient('');
      setMessage('');
      setSender('');
    } else {
      console.error('Socket is not initialized');
    }
  };

  return (
      <div>
        <img src={logo} alt="Encryptodevs_Logo" style={{width: '200px', height: 'auto'}}/>
        <input
            type="text"
            id="send_to_username"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            placeholder="Recipient Username"
        />
        <input
            type="text"
            id="private_message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Private Message"
        />
        <button onClick={handleSendPrivateMessage}>Send Private Message</button>
        <p>Return to <a href="/landing">main page</a></p>
      </div>
  );
};

export default PrivateMessageForm;
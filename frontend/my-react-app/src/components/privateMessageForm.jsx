import React, {useEffect, useState} from 'react';
import io from 'socket.io-client';
import logo from './Encryptodev_Logo.png';
import {useSearchParams} from 'react-router-dom';
import './privateMessageForm.css'; // Import your CSS file


const PrivateMessageForm = () => {
  let [recipient, setRecipient] = useState('');
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  let [sender, setSender] = useState('');
  const [socket, setSocket] = useState(null);
  const [searchParams] = useSearchParams();


  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('No token found, redirecting to login.');
      window.location.href = '/login'; // Redirect to login if no token is found
    }

    const serverUrl = 'http://localhost:5000';
    const newSocket = io(serverUrl, {
      query: {token: token},
    });
    setSocket(newSocket);

    newSocket.on('connect', () => {
      console.log('Socket connected with ID:', newSocket.id);
      newSocket.emit('connected', {socket_id: newSocket.id});
    });

    //

    newSocket.on('new_private_message', (msg) => {
      console.log('New private message received:', msg);
      // Update messages state with the new message
      setMessages(prevMessages => [...prevMessages, msg]);
    });

    return () => {
      newSocket.disconnect();
    };
  }, []);

  const handleSendPrivateMessage = () => {
    if (socket) {
      recipient = searchParams.get('user2')
      sender = searchParams.get('user1')
      console.log(recipient);
      socket.emit('private_message', {recipient, message});
      setRecipient('');
      setMessage('');
      setSender('');
    } else {
      console.error('Socket is not initialized');
    }
  };

  return (
    <div className="chat-page-container">
      <div className="private-message-form-container">
        <img src={logo} alt="Encryptodevs_Logo" />
      </div>
      <div className="chat-container">
        <div className="messages-list">
          <ul>
            {messages.map((msg, index) => (
              <li key={index} className="message">
                {msg}
              </li>
            ))}
          </ul>
        </div>
        <div className="message-input-container">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Private Message"
          />
          <button onClick={handleSendPrivateMessage}>Send Private Message</button>
        </div>
      </div>
      <br />
      <p>Return to <a href="/landing">main page</a></p>
    </div>
  );
};



export default PrivateMessageForm;


import React, { useEffect, useRef, useState } from 'react';
import { io } from 'socket.io-client';

const PrivateMessageForm = () => {
  const [recipient, setRecipient] = useState('');
  const [message, setMessage] = useState('');
  const [sender, setSender] = useState('');
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const newSocket = io();
    setSocket(newSocket);

    newSocket.on('connect', () => {
      newSocket.emit('connected', newSocket.id);
      console.log(`You're now connected on ${newSocket.id}`);
    });

    newSocket.on('new_private_message', (msg) => {
      alert(msg);
    });

    // return () => {
    //   newSocket.disconnect();
    // };
  }, []);

  const handleSendPrivateMessage = () => {
    socket.emit('private_message', { recipient, message, sender });
    setRecipient('Josh');
    setMessage('Hello Test');
    setSender('Ben');
  };

  return (
    <div>
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
      <input
        type="text"
        id="send_from_username"
        value={sender}
        onChange={(e) => setSender(e.target.value)}
        placeholder="Sender Username"
      />
      <button onClick={handleSendPrivateMessage}>Send Private Message</button>
    </div>
  );
};

export default PrivateMessageForm;
import React, { useEffect, useRef, useState } from 'react';
import { io } from 'socket.io-client';

const Chat = () => {
  const [socket, setSocket] = useState(null);
//   const messageContainerRef = useRef(null);

  useEffect(() => {
    const newSocket = io();
    setSocket(newSocket);

    newSocket.on('connect', () => {
      console.log(`You're now connected on ${newSocket.id}`);
      newSocket.emit('connected', newSocket.id);
    });


    newSocket.on('from flask', (msg) => {
      alert(msg);
    });

    newSocket.on('server originated', (msg) => {
      alert(msg);
    });

    newSocket.on('new_private_message', (msg) => {
      alert(msg);
    });

    return () => {
      newSocket.disconnect();
    };
  }, []);

//   const handleMessageSend = (e) => {
//     if (e.key === 'Enter' && socket) {
//       socket.emit('message', e.target.value);
//       e.target.value = '';
//     }
//   };

//   useEffect(() => {
//     if (messageContainerRef.current) {
//       messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;
//     }
//   }, [messages]);

  return (
    <div>
    
      <input
        type="text"
        id="messageInput"
        placeholder="Type your message..."
      />
    </div>
  );
};

export default Chat;

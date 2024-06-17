import React, { useEffect, useRef, useState } from 'react';
import io from 'socket.io-client';
const Chat = () => {
  const [socket, setSocket] = useState(null);
  const [messages, setMessages] = useState([]);
  const messageContainerRef = useRef(null);
  useEffect(() => {
    const newSocket = io();
    setSocket(newSocket);
    newSocket.on('connect', () => {
      const message = "You're connected!";
      setMessages((prevMessages) => [...prevMessages, message]);
      console.log(newSocket.id);
      newSocket.emit('connected', newSocket.id);
    });
    newSocket.on('message', (message) => {
      setMessages((prevMessages) => [...prevMessages, message]);
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
  const handleMessageSend = (e) => {
    if (e.key === 'Enter' && socket) {
      socket.emit('message', e.target.value);
      e.target.value = '';
    }
  };
  useEffect(() => {
    if (messageContainerRef.current) {
      messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;
    }
  }, [messages]);
  return (
    <div>
      <div className="messages" ref={messageContainerRef}>
        {messages.map((message, index) => (
          <p key={index}>{message}</p>
        ))}
      </div>
      <input
        type="text"
        id="messageInput"
        onKeyDown={handleMessageSend}
        placeholder="Type your message..."
      />
    </div>
  );
};
export default Chat;

// import React from 'react';
// import io from 'socket.io-client';

// const socket = io(process.env.REACT_APP_API_URL);


// let messageContainer = document.querySelector(".messages");

// // Sends confirmation message following success connection to the server (i.e., login)
// socket.on('connect', () => {
//     let p = document.createElement("p")
//     p.innerText = ("You're connected!")
//     messageContainer.appendChild(p)
//     console.log(socket.id)
//     let socket_id = socket.id
//     socket.emit("connected", socket_id)
// })


// // Takes user input and sends it to the server, then clears input field
// let messageInput = document.getElementById("messageInput")
// messageInput.addEventListener("keydown", (e) => {
//     if (e.key === 'Enter') {
//         socket.emit("message", messageInput.value)
//         messageInput.value = ""
//     }
// })


// // Displays messages sent from the server in a new <p> tag
// socket.on('message', (message) => {
//     let messageElement = document.createElement("p")
//     messageElement.innerText = message
//     messageContainer.appendChild(messageElement)
// })



// socket.on('from flask', function (msg) {
//     alert(msg);
// });

// socket.on('server originated', function (msg) {
//     alert(msg);
// });


// document.getElementById('send_username').addEventListener('click', function () {
//     const username = document.getElementById('username').value;
//     console.log(username)
//     socket.emit('username', username);
// });


// document.getElementById('send_private_message').addEventListener('click', function () {
//     const recipient = document.getElementById('send_to_username').value;
//     const message_to_send = document.getElementById('private_message').value;
//     const sender = document.getElementById('send_from_username').value;
//     socket.emit('private_message', {'recipient': recipient, 'message': message_to_send, 'sender': sender});
// });

// socket.on('new_private_message', function (msg) {
//     alert(msg);
// });

// const MessagePage = () => {
//     return (
//         <div>
//     <head>
// 		<title>Title</title>
// 	</head>
// 	<body>
// 		<h1>Test</h1>
// 		<div class="messages">
// 			<label for="messageInput"></label><input id="messageInput"/>
// 		</div>
		
// 		<input type="text" id="message"/>
//     <button id="send">Send</button>

//     <input type="text" id="username"/>
//     <button id="send_username">Send Username</button> 

//     <br/>
//     <br/>
//     <br/>

// 	Send From: <input type="text" id="send_from_username"/>
//     Send To: <input type="text" id="send_to_username"/>
//     Message: <input type="text" id="private_message"/>
//     <button id="send_private_message">Send</button>
		
// 		<script src="/static/js/index.js"></script>
// 	</body>
//     </div>
//     );
// };
// export default MessagePage;

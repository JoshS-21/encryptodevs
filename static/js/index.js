const socket = io();

let messageContainer = document.querySelector(".messages");

// Sends confirmation message following success connection to the server (i.e., login)
socket.on('connect', () => {
    let p = document.createElement("p")
    p.innerText = ("You're connected!")
    messageContainer.appendChild(p)
})


// Takes user input and sends it to the server, then clears input field
let messageInput = document.getElementById("messageInput")
messageInput.addEventListener("keydown", (e) => {
    if (e.key === 'Enter') {
        socket.emit("message", messageInput.value)
        messageInput.value = ""
    }
})


// Displays messages sent from the server in a new <p> tag
socket.on('message', (message) => {
    let messageElement = document.createElement("p")
    messageElement.innerText = message
    messageContainer.appendChild(messageElement)
})



socket.on('from flask', function (msg) {
    alert(msg);
});

socket.on('server originated', function (msg) {
    alert(msg);
});


document.getElementById('send_username').addEventListener('click', function () {
    const username = document.getElementById('username').value;
    console.log(username)
    socket.emit('username', username);
});


document.getElementById('send_private_message').addEventListener('click', function () {
    const recipient = document.getElementById('send_to_username').value;
    const message_to_send = document.getElementById('private_message').value;

    socket.emit('private_message', {'username': recipient, 'message': message_to_send});
});

socket.on('new_private_message', function (msg) {
    alert(msg);
});

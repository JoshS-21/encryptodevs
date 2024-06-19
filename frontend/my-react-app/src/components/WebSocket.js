import io from 'socket.io-client';

const initializeWebSocket = () => {
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

    newSocket.on('connect', () => {
        console.log('Socket connected with ID:', newSocket.id);
        newSocket.emit('connected', { socket_id: newSocket.id });
    });

    newSocket.on('new_private_message', (msg) => {
        alert(msg);
    });

    return newSocket;
};

export default initializeWebSocket;
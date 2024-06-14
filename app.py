from flask import request
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import time

# Create a new Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string from .env file
connection_string = os.getenv('MONGODB_URL')

# Initialize the MongoClient
client = MongoClient(connection_string)

# Create (or switch to) a database
db = client['encryptodevs']

# Create a collection and insert a document
message_collection = db['messages']
user_collection = db['users']


# == Your Routes Here ==

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connected')
def connected(socket_id):
    print(socket_id)


@socketio.on('message')
def handle_message(message):
    send(message)


users = {}


@socketio.on('message from user')
def receive_message_from_user(message):
    print('USER MESSAGE: {}'.format(message))
    emit('from flask', message.upper(), broadcast=True)


@socketio.on('username')
def receive_username(username):
    users[username] = request.sid
    # users.append({username : request.sid})
    print(users)
    print('Username added!')


@socketio.on('private_message')
def private_message(payload):
    recipient_session_id = users[payload['recipient']]
    sender_session_id = users[payload['sender']]
    message_content = payload['message']
    message_timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    message_collection.insert_one({"content": message_content, "sender_id": sender_session_id, "recipient_id": recipient_session_id, "timestamp": message_timestamp})
    emit('new_private_message', message_content, room=recipient_session_id)
    emit('new_private_message', message_content, room=sender_session_id)


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    # app.run(debug=True, allow_unsafe_werkzeug=True, port=int(os.environ.get('PORT', 5001)))
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)

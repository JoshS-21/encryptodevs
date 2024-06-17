import os
from flask import Flask, request, render_template, jsonify, session
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
import time
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timezone
from user import User

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# MongoDB's connection string and database name from .env file
connection_string = os.getenv('MONGODB_URL')
encryptodevs = os.getenv('MONGODB_DATABASE')

# Initialize the MongoClient
client = MongoClient(connection_string)
db = client[encryptodevs]
message_collection = db['messages']
user_collection = db['users']

# Enable CORS for all routes
CORS(app)

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    user_data = db['users'].find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_id)
    return None


# Sign-up route
@app.route('/signup', methods=['POST'])
def signup():
    user_data = request.json
    name = user_data.get('name')
    username = user_data.get('username')
    email = user_data.get('email')
    password = user_data.get('password')
    phone_number = user_data.get('phone_number')

    # Save user data to the database
    collection = db['users']
    result = collection.insert_one({
        "name": name,
        "username": username,
        "email": email,
        "password": password,
        "phone_number": phone_number,
        "is_online": False,  # Ensure default value for is_online
        "last_seen": None  # Set last_seen to None at the time of signup
    })

    return jsonify({'message': 'User signed up successfully', 'user_id': str(result.inserted_id)}), 201


# Login route
@app.route('/login', methods=['POST'])
def login():
    user_data = request.json
    username = user_data.get('username')
    password = user_data.get('password')

    collection = db['users']
    user = collection.find_one({'username': username})

    if user and user['password'] == password:
        user_obj = User(str(user['_id']), username)
        user_obj.set_online(True)  # Set user online upon successful login
        collection.update_one({'_id': user['_id']}, {'$set': {'is_online': True, 'last_seen': None}})
        access_token = create_access_token(identity=str(user['_id']))

        return jsonify(
            {'message': 'User logged in successfully', 'user_id': str(user['_id']), 'token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


# Logout route
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user_id = get_jwt_identity()
    db['users'].update_one(
        {'_id': ObjectId(current_user_id)},
        {'$set': {'is_online': False, 'last_seen': datetime.now(timezone.utc).isoformat()}}
    )
    return jsonify({'message': 'User logged out successfully'}), 200


@app.route('/user-status', methods=['GET'])
@jwt_required()
def user_status():
    current_user_id = get_jwt_identity()
    user = db['users'].find_one({'_id': ObjectId(current_user_id)})

    if user:
        return jsonify({
            'username': user['username'],
            'is_online': user.get('is_online', False),
            'last_seen': user.get('last_seen', 'N/A')
        }), 200
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = db['users'].find({}, {'_id': 1, 'username': 1, 'is_online': 1, 'last_seen': 1})
    user_list = []
    for user in users:
        user_list.append({
            'user_id': str(user['_id']),
            'username': user['username'],
            'is_online': user.get('is_online', False),
            'last_seen': user.get('last_seen', 'N/A')
        })
    return jsonify(user_list), 200

@socketio.on('connected')
def connected(socket_id):
    print(socket_id)

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
    recipient_session_id = payload['recipient']
    sender_session_id = payload['sender']
    message_content = payload['message']
    message_timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    message_collection.insert_one({"content": message_content, "sender_id": sender_session_id, "recipient_id": recipient_session_id, "timestamp": message_timestamp})
    emit('new_private_message', message_content, room=recipient_session_id)
    emit('new_private_message', message_content, room=sender_session_id)


if __name__ == '__main__':
    # app.run(debug=True, allow_unsafe_werkzeug=True, port=int(os.environ.get('PORT', 5001)))
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True, debug=True)



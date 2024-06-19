from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS
from datetime import datetime, timedelta

from flask_socketio import SocketIO, send, emit
from datetime import time, timedelta
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
from user import User

import uuid
import requests   
from mailjet_rest import Client

from functools import wraps



# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# MongoDB's connection string and database name from .env file
connection_string = os.getenv('MONGODB_URL')
encryptodevs = os.getenv('MONGODB_DATABASE')
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
MAILGUN_FROM_EMAIL = os.getenv('MAILGUN_FROM_EMAIL')
MAILJET_API_KEY = os.getenv('MAILJET_API_KEY')
MAILJET_API_SECRET = os.getenv('MAILJET_API_SECRET')
MAILJET_FROM_EMAIL = os.getenv('MAILJET_FROM_EMAIL')
# Initialize the MongoClient
client = MongoClient(connection_string)
db = client[encryptodevs]
message_collection = db['messages']
user_collection = db['users']


# Enable CORS for all routes
CORS(app)

def validate_password(password):
    """Validate password against specified criteria."""
    requirements = []
    if len(password) < 7:
        requirements.append('Password must be at least 7 characters long')
    if not any(char.isupper() for char in password):
        requirements.append('Password must include at least one uppercase letter')
    if not any(char in '!@£_%-' for char in password):
        requirements.append('Password must include at least one of !@£_%-')
    return len(requirements) == 0, ', '.join(requirements)



# Sign-up route

@app.route('/signup', methods=['POST'])
def signup():
    user_data = request.json
    name = user_data.get('name')
    username = user_data.get('username')
    email = user_data.get('email')
    password = user_data.get('password')
    phone_number = user_data.get('phone_number')

    # Validate phone number
    if not phone_number.isdigit() or len(phone_number) != 11:
        return jsonify({'message': 'Phone number must be exactly 11 digits long'}), 400

    # Validate password
    is_valid_password, password_message = validate_password(password)
    if not is_valid_password:
        return jsonify({'message': password_message}), 400

    # Check if the username, phone number, or email already exists
    collection = db['users']
    existing_user = collection.find_one(
        {"$or": [{"username": username}, {"phone_number": phone_number}, {"email": email}]})

    if existing_user:
        if existing_user.get('username') == username:
            return jsonify({'message': 'Username already exists'}), 400
        elif existing_user.get('phone_number') == phone_number:
            return jsonify({'message': 'Phone number already exists'}), 400
        elif existing_user.get('email') == email:
            return jsonify({'message': 'Email already exists'}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Save user data to the database
    collection = db['users']
    result = collection.insert_one({
        "name": name,
        "username": username,
        "email": email,
        "password": hashed_password,
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

    if user and bcrypt.check_password_hash(user['password'], password):
        # Login successful
        user_obj = User(str(user['_id']), username)
        user_obj.set_online(True)  # Set user online upon successful login
        collection.update_one({'_id': ObjectId(user['_id'])}, {'$set': {'is_online': True, 'last_seen': None}})
        access_token = create_access_token(identity=str(user['_id']))
        # Store user information in some session management (you might adjust this as per your app's architecture)
        users[username] = {'id': user['_id'], 'email': user['email'], 'phone_number': user['phone_number'],
                           'session_id': None, 'access_token': access_token}
        return jsonify({'message': 'User logged in successfully', 'user_id': str(user['_id']), 'token': access_token}), 200
    elif user is None:
        # Username not found
        return jsonify({'message': 'Username not found. Please sign up to create an account.'}), 401
    else:
        # Incorrect password
        return jsonify({'message': 'Incorrect password'}), 401


# Logout route
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user_id = get_jwt_identity()
    username = user_collection.find_one({'_id': ObjectId(current_user_id)})['username']
    users.pop(username, None)
    db['users'].update_one(
        {'_id': ObjectId(current_user_id)},
        {'$set': {'is_online': False, 'last_seen': time.strftime('%Y-%m-%d %H:%M:%S')}}
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

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')
    user = db['users'].find_one({'email': email})

    if not user:
        return jsonify({'message': 'Email not found'}), 404

    reset_token = str(uuid.uuid4())
    reset_token_expiration = datetime.utcnow() + timedelta(hours=1)

    db['users'].update_one(
        {'_id': user['_id']},
        {'$set': {
            'reset_token': reset_token,
            'reset_token_expiration': reset_token_expiration
        }}
    )

    # Send password reset email with user's name
    send_reset_email(email, reset_token, user['name'])

    return jsonify({'message': 'Password reset email sent'}), 200

@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    reset_token = data.get('reset_token')
    new_password = data.get('new_password')

    # Validate the new password
    is_valid, message = validate_password(new_password)
    if not is_valid:
        return jsonify({'message': message}), 400

    user = db['users'].find_one({'reset_token': reset_token})

    if not user or user['reset_token_expiration'] < datetime.utcnow():
        return jsonify({'message': 'Invalid or expired reset token'}), 400

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

    db['users'].update_one(
        {'_id': user['_id']},
        {'$set': {
            'password': hashed_password,
            'reset_token': None,
            'reset_token_expiration': None
        }}
    )

    return jsonify({'message': 'Password reset successful'}), 200

# Function to send password reset email using Mailjet
def send_reset_email(to_email, token, user_name):
    reset_link = f'http://localhost:3000/reset/{token}'
    subject = 'Reset your password'
    body = f'Hi {user_name},\n\nClick the link below to reset your password:\n\n{reset_link}'

    response = requests.post(
        'https://api.mailjet.com/v3.1/send',
        auth=(MAILJET_API_KEY, MAILJET_API_SECRET),
        json={
            'Messages': [
                {
                    "From": {
                        "Email": MAILJET_FROM_EMAIL,
                        "Name": "Encryptodevs"
                    },
                    "To": [
                        {
                            "Email": to_email,
                            "Name": user_name
                        }
                    ],
                    "Subject": subject,
                    "TextPart": body,
                }
            ]
        }
    )

    if response.status_code == 200:
        print('Password reset email sent successfully.')
    else:
        print(f'Failed to send password reset email: {response.status_code}')
        print(response.text)

# Private Messaging Handler Below
def socket_auth_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            token = request.args.get('token')
            if token:
                decoded_token = decode_token(token)
                user_id = decoded_token['sub']
                request.user_id = user_id  # Attach user_id to request
                return f(*args, **kwargs)
            else:
                raise RuntimeError('Missing token')
        except Exception as e:
            emit('error', {'message': str(e)})
            return

    return wrapped


@socketio.on('connected')
@socket_auth_required
def handle_connected(data):
    user_id = request.user_id
    username = user_collection.find_one({'_id': ObjectId(user_id)})['username']
    socket_id = data['socket_id']
    users[username]['session_id'] = str(socket_id)
    print(users)
    emit('response', {'message': f'User {user_id} connected with socket ID: {socket_id}'})


users = {}


# @socketio.on('username')
# def receive_username(username):
#     users[username] = request.sid
#     # users.append({username : request.sid})
#     print(users)
#     print('Username added!')


@socketio.on('private_message')
@socket_auth_required
def private_message(payload):
    user_id = request.user_id
    username = user_collection.find_one({'_id': ObjectId(user_id)})['username']
    recipient_session_id = users[payload['recipient']]['session_id']
    sender_session_id = users[username]['session_id']
    message_content = payload['message']
    message_timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    message_collection.insert_one(
        {"content": message_content, "sender_id": sender_session_id, "recipient_id": recipient_session_id,
         "timestamp": message_timestamp})
    emit('new_private_message', message_content, room=recipient_session_id)
    emit('new_private_message', message_content, room=sender_session_id)


if __name__ == '__main__':
    # app.run(debug=True)
    # app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True, debug=True)

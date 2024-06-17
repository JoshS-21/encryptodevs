from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timezone
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
from user import User

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# MongoDB's connection string and database name from .env file
connection_string = os.getenv('MONGODB_URL')
encryptodevs = os.getenv('MONGODB_DATABASE')

# Initialize the MongoClient
client = MongoClient(connection_string)
db = client[encryptodevs]

# Enable CORS for all routes
CORS(app)

def validate_password(password):
    """Validate password against specified criteria."""
    if len(password) < 7:
        return False, 'Password must be at least 7 characters long'
    if not any(char.isupper() for char in password):
        return False, 'Password must include at least one uppercase letter'
    if not any(char in '!@£_%-' for char in password):
        return False, 'Password must include at least one of !@£_%-'
    return True, ''

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
    existing_user = collection.find_one({"$or": [{"username": username}, {"phone_number": phone_number}, {"email": email}]})

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


@app.route('/login', methods=['POST'])
def login():
    user_data = request.json
    username = user_data.get('username')
    password = user_data.get('password')

    collection = db['users']
    user = collection.find_one({'username': username})

    if user and bcrypt.check_password_hash(user['password'], password):
        user_obj = User(str(user['_id']), username)
        user_obj.set_online(True)  # Set user online upon successful login
        collection.update_one({'_id': ObjectId(user['_id'])}, {'$set': {'is_online': True, 'last_seen': None}})
        access_token = create_access_token(identity=str(user['_id']))

        return jsonify(
            {'message': 'User logged in successfully', 'user_id': str(user['_id']), 'token': access_token}), 200
    elif user is None:
        return jsonify({'message': 'Username not found. Please sign up to create an account.'}), 401
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

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


if __name__ == '__main__':
    app.run(debug=True)
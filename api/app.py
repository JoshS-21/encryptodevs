import os
from flask import Flask, request, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from user import User

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# MongoDB connection string and database name from .env file
connection_string = os.getenv('MONGODB_URL')
encryptodevs = os.getenv('MONGODB_DATABASE')

# Initialize the MongoClient
client = MongoClient(connection_string)
db = client[encryptodevs]

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize JWT Manager
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id, db)


@app.route('/login', methods=['POST'])
def login():
    try:
        user_data = request.json
        username = user_data.get('username')
        password = user_data.get('password')

        collection = db['users']
        user = collection.find_one({'username': username})

        if user and user['password'] == password:
            user_obj = User(str(user['_id']), username)
            login_user(user_obj)
            user_obj.set_online(True)  # Set user online upon successful login
            collection.update_one({'_id': user['_id']}, {'$set': {'is_online': True}})
            access_token = create_access_token(identity=str(user['_id']))

            # Return a response indicating successful login
            return jsonify({'message': 'User logged in successfully', 'user_id': str(user['_id']), 'token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401

    except Exception as e:
        # Print the error message to the console
        print(f"Error: {str(e)}")
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    try:
        current_user_id = get_jwt_identity()
        # Perform any additional cleanup tasks if needed
        return jsonify({'message': 'User logged out successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500



@app.route('/user-status', methods=['GET'])
@jwt_required()
def user_status():
    current_user_id = get_jwt_identity()
    user = db['users'].find_one({'_id': ObjectId(current_user_id)})

    if user:
        return jsonify({'username': user['username']}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


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
        "phone_number": phone_number
    })

    return jsonify({'message': 'User signed up successfully', 'user_id': str(result.inserted_id)}), 201


if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask, request, jsonify, session
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string and database name from .env file
connection_string = os.getenv('MONGODB_URL')
encryptodevs = os.getenv('MONGODB_DATABASE')

# Initialize the MongoClient
client = MongoClient(connection_string)
db = client[encryptodevs]

# Initialize CORS with your Flask app
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
        "phone_number": phone_number
    })

    return jsonify({'message': 'User signed up successfully', 'user_id': str(result.inserted_id)}), 201


# Login route
@app.route('/login', methods=['POST'])
def login():
    try:
        user_data = request.json
        username = user_data.get('username')
        password = user_data.get('password')

        # Query the database to find the user by username
        collection = db['users']
        user = collection.find_one({'username': username})

        if user and user['password'] == password:
            user_obj = User(str(user['_id']))
            login_user(user_obj)
            return jsonify({'message': 'User logged in successfully', 'user_id': str(user['_id'])}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    logout_user()
    return jsonify({'message': 'User logged out successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)

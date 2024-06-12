import os
from flask import Flask, request, jsonify, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string and database name from .env file
connection_string = os.getenv('MONGODB_URL')
database_name = os.getenv('MONGODB_DATABASE')

# Initialize the MongoClient
client = MongoClient(connection_string)

# Initialize CORS with your Flask app
CORS(app)

db = client["encryptodevs"]

# Sign-up route
@app.route('/signup', methods=['POST'])
def signup():
    user_data = request.json
    name = user_data.get('name')
    username = user_data.get('username')
    email = user_data.get('email')
    password = user_data.get('password')

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Save user data to the database
    collection = db['users']
    result = collection.insert_one({
        "name": name,
        "username": username,
        "email": email,
        "password": hashed_password
    })

    return jsonify({'message': 'User signed up successfully', 'user_id': str(result.inserted_id)}), 201

# Login route
@app.route('/login', methods=['POST'])
def login():
    user_data = request.json
    username = user_data.get('username')
    password = user_data.get('password')

    # Query the database to find the user by username
    collection = db['users']
    user = collection.find_one({'username': username})

    if user and check_password_hash(user['password'], password):
        # Store user ID in the session
        session['user_id'] = str(user['_id'])
        return jsonify({'message': 'User logged in successfully'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session
    session.clear()
    return jsonify({'message': 'User logged out successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)

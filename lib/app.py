import os
from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

# Initialize the Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string and database name from .env file
connection_string = os.getenv('MONGODB_URL')
database_name = os.getenv('MONGODB_DATABASE')

# Initialize the MongoClient
client = MongoClient(connection_string)

# Create (or switch to) the specified database
db = client[database_name]

# Route to insert a sample user document
@app.route('/insert_sample_user', methods=['POST'])
def insert_sample_user():
    # Create a collection and insert a document
    collection = db['users']
    result = collection.insert_one({
        "username": "abdio", 
        "name": "abdi", 
        "email": "abdi@example.com", 
        "phone_number": "123-456-7890", 
        "password": "hashed_password"
    })
    return jsonify({"message": "Inserted document ID: " + str(result.inserted_id)}), 201

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = db['users'].find()
    result = []
    for user in users:
        user_data = {
            "username": user.get("username", "N/A"),
            "name": user.get("name", "N/A"),
            "email": user.get("email", "N/A"),
            "phone_number": user.get("phone_number", "N/A"),
            "password": user.get("password", "N/A")
        }
        result.append(user_data)
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

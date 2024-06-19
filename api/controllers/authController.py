from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from flask_cors import CORS
from models.user import User
import bcrypt
import uuid

from pymongo import MongoClient
import os
connection_string = os.getenv('MONGODB_URL')
encryptodevs = os.getenv('MONGODB_DATABASE')

# Initialize the MongoClient
client = MongoClient(connection_string)
db = client[encryptodevs]

auth = Blueprint('auth', __name__)
CORS(auth, resources={r"/*": {"origins": "http://localhost:3000"}})  # Allow requests from localhost:3000


@auth.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')
    user = db['users'].find_one({'email': email})
    
    if not user:
        return jsonify({'message': 'Email not found'}), 404
    
    reset_token = str(uuid.uuid4())
    db['users'].update_one(
        {'_id': user['_id']},
        {'$set': {
            'reset_token': reset_token,
            'reset_token_expiration': (datetime.utcnow() + timedelta(hours=1)).isoformat()
        }}
    )

    # Send email with the reset token (simplified)
    send_reset_email(user['email'], reset_token)

    return jsonify({'message': 'Password reset email sent'}), 200

@auth.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    reset_token = data.get('reset_token')
    new_password = data.get('new_password')

    user = db['users'].find_one({'reset_token': reset_token})
    
    if not user or datetime.fromisoformat(user['reset_token_expiration']) < datetime.utcnow():
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

def send_reset_email(to_email, token):
    # Here you should use a proper email sending service
    print(f"Send email to {to_email} with reset token {token}")

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import os
connection_string = os.getenv('MONGODB_URL')
encryptodevs = os.getenv('MONGODB_DATABASE')

# Initialize the MongoClient
client = MongoClient(connection_string)
db = client[encryptodevs]

class User:
    @staticmethod
    def find_by_email(email):
        return db.users.find_one({"email": email})

    @staticmethod
    def update_password(email, password):
        hashed_password = generate_password_hash(password)
        db.users.update_one({"email": email}, {"$set": {"password": hashed_password}})

    @staticmethod
    def create(data):
        data['password'] = generate_password_hash(data['password'])
        db.users.insert_one(data)

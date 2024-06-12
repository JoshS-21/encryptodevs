
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string from .env file
connection_string = os.getenv('MONGODB_URL')

# Initialize the MongoClient
client = MongoClient(connection_string)

# Create (or switch to) a database
db = client['encryptodevs']

# Create a collection and insert a document
collection = db['users']
result = collection.insert_one({"username": "abdio", "name": "abdi", "email": "abdi@example.com", "phone_number": "123-456-7890", "password": "hashed_password"})

print("Inserted document ID:", result.inserted_id)

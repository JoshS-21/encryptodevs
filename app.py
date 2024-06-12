import os
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from pymongo import MongoClient
from dotenv import load_dotenv
from lib.user import User
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'encryptodevs'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Ensure Flask-Login redirects to login view

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string and database name from .env file
connection_string = os.getenv('MONGODB_CONNECTION_STRING', 'mongodb://localhost:27017/')
database_name = os.getenv('DATABASE_NAME', 'encryptodevs')

# Initialize the MongoClient
client = MongoClient(connection_string)

# Create (or switch to) the specified database
db = client[database_name]

@login_manager.user_loader
def load_user(user_id):
    try:
        user_data = db['users'].find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(str(user_data['_id']), user_data['name'], user_data['email'], user_data['password'])
    except Exception as e:
        print(f"Error loading user: {e}")
    return None

@app.route('/insert_sample_user', methods=['POST'])
def insert_sample_user():
    collection = db['users']
    result = collection.insert_one({
        "username": "abdio",
        "name": "abdi",
        "email": "abdi@example.com",
        "phone_number": "123-456-7890",
        "password": "hashed_password"
    })
    return jsonify({"message": "Inserted document ID: " + str(result.inserted_id)}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = db['users'].find()
    result = []
    for user in users:
        user_data = {
            "id": str(user.get("_id")),
            "username": user.get("username", "N/A"),
            "name": user.get("name", "N/A"),
            "email": user.get("email", "N/A"),
            "phone_number": user.get("phone_number", "N/A"),
            "password": user.get("password", "N/A")
        }
        result.append(user_data)
    return jsonify(result), 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = db['users'].find_one({"email": email})

        if user_data and user_data['password'] == password:
            user = User(str(user_data['_id']), user_data['name'], user_data['email'], user_data['password'])
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        user_data = {
            "name": name,
            "email": email,
            "password": password
        }
        db['users'].insert_one(user_data)
        flash('Account sign up successful!', 'success')
        return redirect(url_for('login'))

    return render_template('sign_up_form.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

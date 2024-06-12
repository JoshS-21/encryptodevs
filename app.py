import os

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from lib.user import User

from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv


app = Flask(__name__)
app.secret_key = 'encryptodevs'

# Define a static database with sample usernames, emails, and passwords
users = [
    {'id': 1, 'name': 'User One', 'email': 'user1@example.com', 'password': 'password1'},
    {'id': 2, 'name': 'User Two', 'email': 'user2@example.com', 'password': 'password2'}]

login_manager = LoginManager()  # Create a LoginManager instance
login_manager.init_app(app)  # Initialize the LoginManager with the Flask application instance


@login_manager.user_loader
def load_user(user_id):
    user_data = next((user for user in users if str(user['id']) == user_id), None)
    if user_data:
        return User(str(user_data['id']), user_data['name'], user_data['email'], user_data['password'])
    return None


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Redirect user if already logged in
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = next((user for user in users if user['email'] == email), None)

        if user_data and user_data['password'] == password:
            user = User(str(user_data['id']), user_data['name'], user_data['email'], user_data['password'])
            login_user(user)  # Log in the user
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

        # Check if the email already exists
        if any(user['email'] == email for user in users):
            flash('Email already exists. Please use a different email or sign in.', 'error')
            return render_template('sign_up_form.html')  # Render the sign-up form with the flash message

        # If the email doesn't exist, create the user
        user_id = len(users) + 1
        users.append({'id': user_id, 'name': name, 'email': email, 'password': password})
        flash('Account sign up successful!', 'success')  # Flash success message
        return redirect(url_for('login'))

    return render_template('sign_up_form.html')


@app.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:  # Redirect user if not logged in
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=current_user)


@app.route('/logout', methods=['GET'])
def return_to_login():
    logout_user()
    return redirect('/login')  #Redirect back to login page


if __name__ == '__main__':
    app.run(debug=True)


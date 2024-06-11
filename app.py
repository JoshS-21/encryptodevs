import os
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user
from lib.user import User

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


@app.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:  # Redirect user if not logged in
        return redirect(url_for('login'))

    return render_template('dashboard.html', user=current_user)


if __name__ == '__main__':
    app.run(debug=True)

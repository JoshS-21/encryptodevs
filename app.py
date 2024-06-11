import os
from flask import Flask, request, render_template, redirect, url_for, flash

from encryptodevs.lib.user import User
from lib.database_connection import get_flask_database_connection
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from lib.user_repository import UserRepository
import datetime

app = Flask(__name__)  # Create a Flask application instance
app.secret_key = 'encryptodevs'  # Set a secret key for the application

login_manager = LoginManager()  # Create a LoginManager instance
login_manager.init_app(app)  # Initialize the LoginManager with the Flask application instance


@login_manager.user_loader  # Register a user loader function with the LoginManager
def load_user(user_id):  # Define a function to load a user given a user id
    connection = get_flask_database_connection(app)
    repo = UserRepository(connection)
    user_data = repo.find(user_id)
    if user_data:
        return User(user_data.id, user_data.name, user_data.email, user_data.password)
    return None


#LINK: http://127.0.0.1:5001/login

# -------------------------------------------------LOGIN page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']  # Retrieve the email from the form data
        password = request.form['password']  # Retrieve the password from the form data
        connection = get_flask_database_connection(app)
        users = UserRepository(connection)
        users2 = users.all()
        for user in users2:  # Iterate over the users dictionary
            if user.email == email and user.password == password:
                user = User(user.id, user.name, email, password)
                login_user(user)
                return render_template('dashboard.html', user=user)

        # If email or password is incorrect, show flash message
        flash('Invalid email or password. Please try again.', 'error')
        return redirect("/login")

    return render_template('login.html')


# -------------------------------------------------LOGIN page


# -------------------------------------------------SIGN UP page
@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        password_confirmation = request.form['password_conf']
        connection = get_flask_database_connection(app)
        users = UserRepository(connection)

        # Check if the email already exists
        if users.check_email_exists(email):
            flash('Email already exists. Please use a different email or sign in.', 'error')
            return redirect('/dashboard')  # Render the sign-up form with the flash message

        if password != password_confirmation:
            flash('Passwords are not the same')
            return redirect('/dashboard')

        # If the email doesn't exist, create the user
        users.create(User(None, name, email, password))
        flash('Account sign up successful!', 'success')  # Flash success message
        return redirect("/login")

    return redirect('/dashboard')


# -------------------------------------------------SIGN UP page

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))

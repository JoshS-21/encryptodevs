import os
from flask import Flask, request, render_template, redirect, url_for
from lib.database_connection import get_flask_database_connection
from lib.peep_repository import PeepRepository
from lib.peep import Peep
from lib.user_repository import UserRepository
from lib.user import User


# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==


# == Example Code Below ==

# GET /emoji
# Returns a smiley face in HTML
# Try it:
#   ; open http://localhost:5001/emoji

# app route for chitter homepage
@app.route('/chitter/home', methods=['GET'])
def get_chitter_homepage():
    return render_template('home.html')

# app route to GET sign up page
@app.route('/chitter/user/sign_up', methods=['GET'])
def get_login_sign_up_page():
    return render_template('new_user.html')

# app route for POST request of the sign up page
@app.route('/chitter/user/sign_up', methods=['POST'])
def create_account():
    # Set up the database connection and repository
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)

    # Get the fields from the request form
    name = request.form ['name']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # SQL query to check if username or email already exist as both must be unique
    username_check = connection.execute('SELECT * from users WHERE username = %s', [username])
    email_check = connection.execute('SELECT * from users WHERE email = %s', [email])
    # This if is checking to see if the sql query has found an instance of the username or email
    # If the username_check or email_check has found an entry then it will render the signup_failed.html
    if username_check or email_check:
        return render_template('signup_failed_username_email_notunique.html')
    # This else is if the entered username or email has not already in the database and then creates the user account
    else:
        if "@" in email and "." in email:
            if len(password) >= 8 and any(char.isupper() == True for char in password):
        # Create a user object
                user = User(None, name, username, email, password)
                
                # Save the user to the database
                user_repository.create(user)
                rows = connection.execute('SELECT * from users WHERE username = %s', [username])
                id = rows[0]['id']
                

                # Redirect to the welcome page with their id
                return redirect(f"/welcome/{id}")
            else:
                return render_template('signup_failed_password.html')
        else:
            return render_template('signup_failed_email.html')

# GET request to render the login.html page
@app.route('/chitter/user/login', methods=['GET'])
def get_login_page():
    return render_template('login.html')

# POST request has forms to take in user ifo for login
@app.route('/chitter/user/login', methods=['POST'])
def login_account():
    # Set up the database connection and repository
    connection = get_flask_database_connection(app)

    # Get the fields from the request form
    username = request.form['username']
    password = request.form['password']

    # SQL commamnd to check if the username is in the databse
    username_check = connection.execute('SELECT * from users WHERE username = %s', [username])
    # If username is found
    if username_check:
        # This check to see if the password enetered in the password field is the same as the password in the database
        if password == username_check[0]['password']:
            id = username_check[0]['id']
            # Redirects to the users welcome page
            return redirect(f"/welcome/{id}")
        else:
            # If the username is found but the password incorect the user will be promted to re enter details untill correct.
            return render_template('login_failed.html')
    # if username is not found return to the login page, where they will also have an option to create an account.    
    else:
        return render_template('login_failed.html')

# app route for welcome page that is user specific
@app.route('/welcome/<int:id>', methods=['GET'])
def welcome_page(id):
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)
    user_info = repository.find(id)
    return render_template('welcome.html', user = user_info)
    
# app route for retrieving all peeps their id is taken as they may create a peep from this page and the id will be used to assign to the peep
@app.route('/get_all_peeps/<int:id>', methods=['GET'])
def get_peeps(id):
    connection = get_flask_database_connection(app)
    peep_repository = PeepRepository(connection)
    peep_list = peep_repository.all()
    return render_template('get_peeps.html', peeps = peep_list, id = id)

# app route for view peep in view only mode when the user is not logged in
@app.route('/chitter/view_peeps', methods=['GET'])
def view_peeps():
    connection = get_flask_database_connection(app)
    peep_repository = PeepRepository(connection)
    peep_list = peep_repository.all()
    return render_template('view_peeps.html', peeps = peep_list)

# app route for GET request to render the new_peep.html page
@app.route('/peep/new/<int:id>', methods=['GET'])
def get_new_peep(id):
    connection = get_flask_database_connection(app)
    return render_template('new_peep.html', id = id)

# POST request to retireve all the information to create a peep
@app.route('/peep_create/<int:id>', methods=['POST'])
def create_peep(id):
    # Set up the database connection and repository
    connection = get_flask_database_connection(app)
    peep_repository = PeepRepository(connection)

    # Get the fields from the request form
    message = request.form['message']
    tag = request.form['tag']

    # Create a peep object
    peep = Peep(None, message, None, id, tag)
    
    # Save the peep to the database
    peep_repository.create(peep)

    # Redirect to the get all peeps route so user can see it 
    return redirect(f'/get_all_peeps/{id}')

# app route for about_peep to view more information on the peep. /peep.id/user.id user.id is required so that when the user goes back to the get all peep page they will return to their user specific in case they then go on to create another peep
@app.route('/about_peep/<int:id>/<int:id1>', methods=['GET'])
def find_peep_info(id, id1):
    connection = get_flask_database_connection(app)
    peep_repository = PeepRepository(connection)
    peep_info = peep_repository.find(id)
    return render_template('about_peep.html', peep = peep_info, id = id1)

@app.route('/about_peep_view/<int:id>', methods=['GET'])
def view_peep_info(id):
    connection = get_flask_database_connection(app)
    peep_repository = PeepRepository(connection)
    peep_info = peep_repository.find(id)
    return render_template('view_about_peep.html', peep = peep_info)

# == End Example Code ==

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))

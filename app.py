from flask_socketio import emit
import os
from flask import Flask, request, render_template, redirect, url_for
from flask_socketio import SocketIO, emit, send

# Create a new Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# == Your Routes Here ==

@app.route('/')
def index():
    return render_template('index.html')


# @socketio.on('connect')
# def test_connect():
#     emit('my response', {'data': 'Connected'})


# @socketio.on('message')
# def handle_message(message):
#     send(message)


# @socketio.on('message')
# def response(auth):
#     emit('connected')
#     print()


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    # app.run(debug=True, allow_unsafe_werkzeug=True, port=int(os.environ.get('PORT', 5001)))
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)

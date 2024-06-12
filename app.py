from flask import request
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

# Create a new Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# == Your Routes Here ==

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(message):
    print(request.sid)
    send(message)


users = {}


@socketio.on('message from user')
def receive_message_from_user(message):
    print('USER MESSAGE: {}'.format(message))
    emit('from flask', message.upper(), broadcast=True)


@socketio.on('username')
def receive_username(username):
    users[username] = request.sid
    # users.append({username : request.sid})
    print(users)
    print('Username added!')


@socketio.on('private_message')
def private_message(payload):
    recipient_session_id = users[payload['username']]
    message = payload['message']

    emit('new_private_message', message, room=recipient_session_id)


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    # app.run(debug=True, allow_unsafe_werkzeug=True, port=int(os.environ.get('PORT', 5001)))
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)

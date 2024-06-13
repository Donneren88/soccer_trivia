from flask import Flask, render_template, session, redirect, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trivia')
def trivia():
    return render_template('trivia.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)

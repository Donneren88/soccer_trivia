from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models import User  # Ensure the User model is imported
    from .routes import main, trivia  # Correct import of the main and trivia blueprints
    from .auth.routes import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(trivia)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Ensure the User model is imported
    return User.query.get(int(user_id))

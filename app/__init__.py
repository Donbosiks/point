from flask import Flask
from datetime import timedelta
from flask_login import LoginManager, UserMixin
from dotenv import load_dotenv
import os
from app.sqlite_model import init_db

class User(UserMixin):
    def __init__(self, id):
        self.id = id


def create_app():
    init_db()
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    load_dotenv()
    app.secret_key = os.getenv('SECRET_KEY')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    from .admin import admin_bp
    from .user import user_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)

    # Устанавливаем время жизни сессии в LOGIN_TIME часаx
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=int(os.getenv('LOGIN_TIME')))

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    return app
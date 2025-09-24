from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    # It's important to keep the key in an environment variable
    # For simplicity of this project, it will be hardcoded
    app.config['SECRET_KEY'] = 'a-very-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wms.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    from wms.routes import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        from . import models
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    return app

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)
    flask_bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        # Import Blueprints
        from .routes.users_route import users_bp
        from .routes.messages_route import messages_bp

        # REGISTER ROUTES
        app.register_blueprint(users_bp, url_prefix="/users")
        app.register_blueprint(messages_bp, url_prefix="/messages")


        return app
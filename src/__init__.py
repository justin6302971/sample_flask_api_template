from flask import Flask
import os
from src.controllers.auth import auth
from src.controllers.bookmarks import bookmarks
from src.db.database import db
from flask_jwt_extended import JWTManager

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI'),
            SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS'),
            SQLALCHEMY_ECHO=os.environ.get('SQLALCHEMY_ECHO') == 'True',
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
        )

    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)


    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    return app

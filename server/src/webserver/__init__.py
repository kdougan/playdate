"""Main app."""

import json
import os
import sys

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .controllers.auth import AuthController
from .. import config
from .extensions import cache
from .database import db
from .depot import setup_depot
from .routes import Router


def create_app(config=config.BaseConfig):
    """Return an initialized Flask application."""
    app = Flask(__name__, template_folder='static')
    app.config.from_object(config)
    CORS(app, supports_credentials=True)

    jwt_manager = JWTManager(app)
    @jwt_manager.user_loader_callback_loader
    def get_current_user(person_id):
        return AuthController.current_user_loader(person_id)

    app.url_map.strict_slashes = False

    register_extensions(app)
    register_routes(app)
    setup_depot(app)

    return app


def register_extensions(app):
    """Register extensions with the Flask application."""
    db.init_app(app)
    cache.init_app(app)


def register_routes(app):
    """Register routes with the Flask application."""
    Router(app)

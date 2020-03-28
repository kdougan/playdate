"""Main app."""

import sys
import os
import json

from flask import Flask

from .. import config
from .routes import Router
from .models import db

from .extensions import redis_store


def create_app(config=config.BaseConfig):
    """Return an initialized Flask application."""
    app = Flask(__name__, template_folder='static')
    app.config.from_object(config)
    # CORS(app, supports_credentials=True)
    app.url_map.strict_slashes = False

    register_extensions(app)
    register_routes(app)

    return app


def register_extensions(app):
    """Register extensions with the Flask application."""
    db.init_app(app)
    redis_store.init_app(app)

def register_routes(app):
    """Register routes with the Flask application."""
    Router(app)
   
"""Routes Initializer."""

from flask_restful import Api
from flask import Blueprint

from . import client
from .api import v1


class Router(object):
    """Router class."""

    api_blueprint = Blueprint('api', __name__)

    def __init__(self, app=None):
        """Initialize the class."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize with app."""
        self._init_client_resources(app)

        prefix = app.config['API_URL_PREFIX']
        api = Api(self.api_blueprint, prefix=prefix)
        self._init_api_resources(api)

        app.register_blueprint(self.api_blueprint)

    def _init_client_resources(self, app):
        client.register(app)

    def _init_api_resources(self, api):
        v1.register(api)

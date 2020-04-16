"""Routes Initializer."""

from flask import Blueprint
from flask_graphql import GraphQLView
from flask_restful import Api
from flask_restful.utils import cors

from . import client
from .api import v1
# from ..graphql import schema


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
        api.decorators = [cors.crossdomain(origin='*')]
        self._init_api_resources(api)

        app.register_blueprint(self.api_blueprint)

        # app.add_url_rule(
        #     '/graphql',
        #     view_func=GraphQLView.as_view(
        #         'graphql',
        #         schema=schema,
        #         graphiql=True  # for having the GraphiQL interface
        #     )
        # )

    def _init_client_resources(self, app):
        client.register(app)

    def _init_api_resources(self, api):
        v1.register(api)

"""Auth Routes."""

import json

from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_refresh_token_required

from src.webserver.controllers import AuthController
from src.webserver.routes._request_parser import RequestParser


def register(api):
    """Resource registration."""
    api.add_resource(AuthRoute, '/v1/auth')
    api.add_resource(AuthRefreshRoute, '/v1/auth/refresh')
    api.add_resource(AuthVerifyRoute, '/v1/auth/verify')


class AuthRoute(Resource):
    """User Route."""

    def post(self):
        """Post method."""
        parser = RequestParser()
        parser.add_argument('email', type=str, required=True,
                            help='missing [email]')
        parser.add_argument('password', type=str, required=True,
                            help='missing [password]')
        kwargs = parser.parse_args()
        controller = AuthController()
        return controller.authenticate(**kwargs)


class AuthRefreshRoute(Resource):
    """User Route."""

    @jwt_refresh_token_required
    def post(self):
        """Post method."""
        controller = AuthController()
        return controller.refresh()


class AuthVerifyRoute(Resource):
    """User Route."""

    @jwt_required
    def post(self):
        """Post method."""
        return 'OK', 200

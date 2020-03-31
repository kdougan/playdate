"""Apple Pay Routes."""

import json

from flask import Response
from flask import abort
from flask import session
from flask_restful import Resource

from src.webserver.controllers.user import UserController
from src.webserver.routes._request_parser import RequestParser


def register(api):
    """Resource registration."""
    api.add_resource(UsersRoute, '/v1/user')
    api.add_resource(UserRoute, '/v1/user/<username>')


class UsersRoute(Resource):
    """User Route."""

    def get(self):
        """Get method."""
        uc = UserController()
        return uc.get()

    def post(self):
        """Post method."""

        parser = RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='missing [name]')
        parser.add_argument('email', type=str, required=True,
                            help='missing [email]')
        parser.add_argument('password', type=str, required=True,
                            help='missing [password]')
        parser.add_argument('username', type=str)
        parser.add_argument('allow_streaming', type=bool, default=True)
        kwargs = parser.parse_args()
        uc = UserController()
        return uc.create(**kwargs)


class UserRoute(Resource):
    """User Route."""

    def get(self, username):
        """Get method."""
        uc = UserController()
        return uc.get(username)

    def delete(self, username):
        uc = UserController()
        return uc.delete(username)

    def put(self, username):
        parser = RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('allow_streaming', type=bool)
        parser.add_argument('active', type=bool)
        parser.add_argument('hidden', type=bool)
        kwargs = parser.parse_args()
        uc = UserController()
        return uc.update(username, **kwargs)

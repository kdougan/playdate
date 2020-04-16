"""People Routes."""

import json

from flask import Response
from flask import abort
from flask import request
from flask import session
from flask_jwt_extended import jwt_optional
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from src.webserver.controllers import PersonController
from src.webserver.extensions import cache
from src.webserver.routes._request_parser import RequestParser
from werkzeug.datastructures import FileStorage


def register(api):
    """Resource registration."""
    api.add_resource(PersonConfigRoute, '/v1/config')
    api.add_resource(PersonRoute,
                     '/v1/person',
                     '/v1/person/<person_id>')
    api.add_resource(PersonAvatarRoute, '/v1/person/<person_id>/avatar')
    api.add_resource(PersonSubRoute, '/v1/person/subscribe')


class PersonRoute(Resource):
    """Person Route."""

    @jwt_optional
    def get(self, person_id=None):
        """Get method."""
        controller = PersonController()
        return controller.get(person_id)

    @jwt_required
    def delete(self):
        """Delete method."""
        parser = RequestParser()
        parser.add_argument('person_id', type=str)
        kwargs = parser.parse_args()
        controller = PersonController()
        return controller.delete(**kwargs)

    @jwt_required
    def put(self, handle):
        """Put method."""
        parser = RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('allow_streaming', type=bool)
        parser.add_argument('active', type=bool)
        parser.add_argument('hidden', type=bool)
        kwargs = parser.parse_args()
        controller = PersonController()
        return controller.update(handle, **kwargs)

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
        parser.add_argument('asset', type=FileStorage)
        kwargs = parser.parse_args()
        controller = PersonController()
        return controller.create(**kwargs)


class PersonConfigRoute(Resource):
    """Person Config Route."""
    @jwt_optional
    @cache.memoize(50)
    def get(self):
        controller = PersonController()
        return controller.get_config()


class PersonSubRoute(Resource):
    """Person Subscription Route."""

    @jwt_required
    def post(self):
        parser = RequestParser()
        parser.add_argument('entity_id', type=str, required=True,
                            help='missing [entity_id]')
        parser.add_argument('action', type=str, required=True,
                            help='missing [action]')
        kwargs = parser.parse_args()
        controller = PersonController()
        return controller.subscribe(**kwargs)


class PersonAvatarRoute(Resource):
    """Person Avatar Route."""

    def put(self, person_id):
        parser = RequestParser()
        parser.add_argument('file', required=True,
                            help='missing [file]')
        kwargs = parser.parse_args()
        controller = PersonController()
        return controller.set_asset(person_id, **kwargs)

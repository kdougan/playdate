import json

from flask import Response
from flask import abort
from flask import session
from flask_restful import Resource

from src.webserver.controllers.group import GroupController
from src.webserver.routes._request_parser import RequestParser


def register(api):
    """Resource registration."""
    api.add_resource(GroupsRoute, '/v1/group')
    api.add_resource(GroupRoute, '/v1/group/<group_id>')


class GroupsRoute(Resource):
    """User Route."""

    def get(self):
        """Get method."""
        controller = GroupController()
        return controller.get()

    def post(self):
        """Post method."""

        parser = RequestParser()

        parser.add_argument('event_id', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('host', type=str)
        parser.add_argument('slotCount', type=int)
        parser.add_argument('name', type=str, required=True,
                            help='missing [name]')
        parser.add_argument('email', type=str, required=True,
                            help='missing [email]')
        parser.add_argument('password', type=str, required=True,
                            help='missing [password]')
        parser.add_argument('username', type=str)
        parser.add_argument('allow_streaming', type=bool, default=True)
        kwargs = parser.parse_args()
        controller = GroupController()
        return controller.create(**kwargs)


class GroupRoute(Resource):
    """User Route."""

    def get(self, group_id):
        """Get method."""
        controller = GroupController()
        return controller.get(group_id)

    def put(self):
        """Put method."""
        controller = GroupController()
        return controller.create(**kwargs)

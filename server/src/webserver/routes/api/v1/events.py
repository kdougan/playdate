import json
from datetime import datetime

from flask import Response
from flask import abort
from flask import session
from flask_restful import Resource
from flask_jwt_extended import jwt_required


from src.webserver.controllers.event import EventController
from src.webserver.routes._request_parser import RequestParser


def register(api):
    """Resource registration."""
    api.add_resource(EventsRoute, '/v1/event')
    api.add_resource(EventRoute, '/v1/event/<event_id>')


class EventsRoute(Resource):
    """Events Route."""

    def get(self):
        """Get method."""
        parser = RequestParser()
        parser.add_argument('start_time', type=datetime, required=True,
                            help='missing [start_time]')
        parser.add_argument('end_time', type=datetime, required=True,
                            help='missing [end_time]')
        kwargs = parser.parse_args()
        controller = EventController()
        return controller.get(**kwargs)

    @jwt_required
    def post(self):
        """Post method."""
        parser = RequestParser()
        parser.add_argument('title', type=str, required=True,
                            help='missing [title]')
        parser.add_argument('description', type=str, required=True,
                            help='missing [description]')
        parser.add_argument('start_time', type=datetime, required=True,
                            help='missing [start_time]')
        parser.add_argument('duration', type=int, required=True,
                            help='missing [duration]')
        parser.add_argument('private', type=bool, default=False)
        kwargs = parser.parse_args()
        controller = EventController()
        return controller.create(**kwargs)


class EventRoute(Resource):
    """Event Route."""

    def get(self, event_id):
        """Get method."""
        controller = EventController()
        return controller.get(event_id=event_id)

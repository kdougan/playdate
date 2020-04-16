"""Event Routes."""

import json
from datetime import datetime

from flask import Response
from flask import abort
from flask import session
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from src.webserver.extensions import cache
from src.webserver.controllers import EventController
from src.webserver.routes._request_parser import RequestParser


def register(api):
    """Resource registration."""
    api.add_resource(EventsRoute, '/v1/event')
    api.add_resource(EventRoute, '/v1/event/<event_id>')
    api.add_resource(EventAvatarRoute, '/v1/event/<event_id>/splash')
    api.add_resource(EventSubscribeRoute, '/v1/event/<event_id>/subscribe')


class EventsRoute(Resource):
    """Events Route."""

    @jwt_required
    @cache.memoize(50)
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
        parser.add_argument('calendar_id', type=int, required=True,
                            help='missing [calendar_id]')
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

    @jwt_required
    def put(self, event_id):
        """Put method."""
        parser = RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('owner', type=str)
        parser.add_argument('start_time', type=datetime)
        parser.add_argument('duration', type=int)
        parser.add_argument('private', type=bool)
        kwargs = parser.parse_args()
        controller = EventController()
        return controller.update(event_id, **kwargs)


class EventSubscribeRoute(Resource):
    """Event Subscribe."""

    @jwt_required
    def post(self, event_id):
        controller = EventController()
        return controller.subscribe(event_id)

    @jwt_required
    def delete(self, event_id):
        controller = EventController()
        return controller.unsubscribe(event_id)


class EventAvatarRoute(Resource):
    """Event Avatar Route."""

    def put(self, event_id):
        parser = RequestParser()
        parser.add_argument('file', required=True,
                            help='missing [file]')
        kwargs = parser.parse_args()
        controller = EventController()
        return controller.set_asset(event_id, **kwargs)

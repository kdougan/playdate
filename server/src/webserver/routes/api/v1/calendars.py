"""Calendar Routes."""

import json

from flask_restful import Resource
from flask_jwt_extended import jwt_required

from src.webserver.controllers import CalendarController
from src.webserver.routes._request_parser import RequestParser


def register(api):
    """Resource registration."""
    api.add_resource(CalendarRoute, '/v1/calendar')
    api.add_resource(CalendarSubscribeRoute,
                     '/v1/calendar/<int:calendar_id>/subscribe')
    api.add_resource(CalendarSubscriptionRoute,
                     '/v1/calendar/<int:calendar_id>/subscription')
    api.add_resource(CalendarUnsubscribeRoute,
                     '/v1/calendar/<int:calendar_id>/unsubscribe')


class CalendarRoute(Resource):
    """Calendar Route."""

    def post(self):
        """Post method."""
        parser = RequestParser()
        parser.add_argument('private', type=bool)
        kwargs = parser.parse_args()
        controller = CalendarController()
        return controller.create(**kwargs)


class CalendarSubscribeRoute(Resource):
    """Calendar Subscribe."""

    @jwt_required
    def post(self, calendar_id):
        controller = CalendarController()
        return controller.subscribe(calendar_id)


class CalendarUnsubscribeRoute(Resource):
    """Calendar Unsubscribe."""

    @jwt_required
    def post(self, calendar_id):
        controller = CalendarController()
        return controller.unsubscribe(calendar_id)


class CalendarSubscriptionRoute(Resource):

    @jwt_required
    def put(self, calendar_id):
        parser = RequestParser()
        parser.add_argument('color', type=str)
        kwargs = parser.parse_args()
        controller = CalendarController()
        return controller.update_subscription(calendar_id, **kwargs)

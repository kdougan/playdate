"""Admin Routes."""

from flask_restful import Resource
from flask_jwt_extended import jwt_required


from src.webserver.routes._util import verify_access
from src.webserver.routes._request_parser import RequestParser

from src.webserver.controllers import AdminController


def register(api):
    """Resource registration."""
    api.add_resource(AdminEventRoute, '/v1/admin/event/<event_id>')


class AdminEventRoute(Resource):

    @jwt_required
    @verify_access('admin')
    def put(self, event_id):
        parser = RequestParser()
        parser.add_argument('action', str, required=True,
                            help='missing parameter [action]')
        parser.add_argument('payload', dict, required=True,
                            help='missing parameter [payload]')
        kwargs = parser.parse_args()
        controller = AdminController()
        if kwargs['action'] == 'setEventCalendar':
            return controller.set_event_calendar(event_id, kwargs['payload'].get('calendarId'))

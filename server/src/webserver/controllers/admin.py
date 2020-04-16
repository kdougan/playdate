"""Admin Controller."""

import json
from flask import abort
from http import HTTPStatus

from flask_jwt_extended import current_user

from ..models.event import Event
from ..models.calendar import Calendar


class AdminController:

    def __init__(self):
        """Initialize the class."""
        pass

    def set_event_calendar(self, event_id, new_owner_id):
        calendar = Calendar.get_or_404(new_owner_id)
        event = Event.get_or_404(event_id)
        event.calendar = calendar
        event.save()
        return event

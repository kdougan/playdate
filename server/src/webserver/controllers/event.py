"""Event Controller."""

import json
import time
from datetime import datetime
from datetime import timedelta

from flask import abort
from flask import current_app
from flask_jwt_extended import get_jwt_identity

from ..models import Event
from ..models import User
from . import hash_password
from . import verify_password


class EventController:
    """GroupController Class."""

    def __init__(self):
        """Initialize the class."""
        pass

    def get(self, event_id=None, start_time=None, end_time=None):
        """Return Group information by id."""
        if event_id:
            return json.loads(Event.objects(id=event_id).first_or_404().to_json())
        if start_time and end_time:
            events = Event.time_range(start_time, end_time)
            return list(map(lambda e: json.loads(e.to_json()), events))
        abort(400,
              'you must specify either an [event_id] or [start_time] and [end_time] pair')

    def create(self, title, description, start_time, duration, private=False):
        end_time = start_time + timedelta(minutes=duration)
        event = Event(
            title=title,
            description=description,
            owner=get_jwt_identity(),
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            private=private
        )
        event.save()
        return json.loads(event.to_json())

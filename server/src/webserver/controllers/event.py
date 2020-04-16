"""Event Controller."""

import copy
import json
import time
from datetime import datetime
from datetime import timedelta

from flask import abort
from flask_jwt_extended import current_user
from sqlalchemy import or_

from src.webserver.database import db
from ..models.calendar import Calendar
from ..models.event import Event
from ..models.person import Person
from ..models.person import PersonRole
from ..models.join import PersonEventSub
from ._util import Color

IMAGE_MIME_TYPES = {
    'image/jpeg',
    'image/png'
}


class EventController:
    """GroupController Class."""

    def __init__(self):
        """Initialize the class."""
        pass

    def get(self, event_id=None, start_time=None, end_time=None):
        """Return Group information by id."""
        if event_id:
            return Event.get_or_404(event_id).expanded()

        if start_time and end_time:
            events = self.events_for_time_range(start_time, end_time)
            if not events:
                return []
            person_calendar = current_user.calendar
            calendar_subs = {
                sub.calendar_id: sub for sub in current_user.calendar_subscriptions}
            event_subs = {
                sub.event_id: sub for sub in current_user.event_subscriptions}
            events = filter(lambda event: (
                event.calendar_id == person_calendar.id or
                event.calendar_id in calendar_subs or
                event.id in event_subs
            ), events)
            data = []
            for e in events:
                event = e._dict()
                event['owner_id'] = e.calendar.owner_id
                event['color'] = calendar_subs.get(
                    e.calendar_id,
                    event_subs.get(
                        e.id,
                        person_calendar)).meta.get('color')
                data.append(event)
            return data
        abort(400,
              'you must specify either an [event_id] or a [start_time] and [end_time] pair')

    def events_for_time_range(self, start_time, end_time):
        return db.session.query(
            Event
        ).filter(
            or_(
                Event.start_time <= end_time,
                Event.end_time >= start_time
            )
        ).all()

    def create(self, calendar_id, title, description, start_time, duration, private=False, meta={}):
        calendar = Calendar.get_or_404(calendar_id)
        if calendar.owner != current_user and current_user.role.value <= PersonRole.moderator.value:
            abort(403, 'person is not authorized to create events for other people')
        end_time = start_time + timedelta(minutes=duration)
        event = Event(
            title=title,
            description=description,
            calendar_id=calendar_id,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            private=private,
            meta=meta
        )
        db.session.add(event)
        db.session.commit()
        db.session.refresh(event)
        return event, 201

    def update(self, event_id, **kwargs):
        event = Event.objects(event_id).first_or_404()
        changed = False
        for k, v in kwargs.items():
            if not hasattr(event, k):
                abort(400, f'unknown key: "{k}"')
            current_value = getattr(event, k)
            if k != current_value:
                setattr(event, k, v)
                changed = True
        if changed:
            event.save()
        return json.loads(event.to_json())

    def subscribe(self, event_id, person_id=None):
        event = Event.get_or_404(event_id)
        person = Person.get_or_404(person_id) if person_id else current_user
        try:
            subscription = PersonEventSub.create(
                person_id=person.id,
                event_id=event.id,
                meta={'color': Color.random()})
        except:
            abort(400, f'unable to subscribe to event {event_id}')
        return subscription, 201

    def unsubscribe(self, event_id, person_id=None):
        event = Event.get_or_404(event_id)
        person = Person.get_or_404(person_id) if person_id else current_user
        sub = db.session.query(PersonEventSub).filter(
            PersonEventSub.person_id == person.id,
            PersonEventSub.event_id == event.id
        ).first()
        if not sub:
            abort(
                400, f'person {person.id} not subscribed to event {event_id}')
        sub.delete()
        return True

    def set_asset(self, event_id, file=None):
        event = Event.get_or_404(event_id)
        if file:
            mime_types = set(file.content_type.split(','))
            is_mime_type_allowed = any(
                mime_types.intersection(IMAGE_MIME_TYPES))

            if not is_mime_type_allowed:
                abort(HTTPStatus.BAD_REQUEST,
                      f'only files of type {IMAGE_MIME_TYPES} supported')
        event.asset = file
        event.save(refresh=True)
        return event

"""Calendar Controller."""

import json
import time
import copy

from http import HTTPStatus
from flask import abort
from flask_jwt_extended import current_user

from src.webserver.database import db
from ..models.calendar import Calendar
from ..models.join import PersonCalendarSub
from ..models.person import Person
from ._util import Color


class CalendarController:
    """CalendarController Class."""

    def __init__(self):
        """Initialize the class."""
        pass

    def get(self, calendar_id):
        """Return Group information by id."""
        return Calendar.get_or_404(calendar_id)

    def create(self, private=False):
        calendar = Calendar.create(
            owner_id=current_user.id,
            private=private,
            meta={'color': Color.random()})
        return calendar, 201

    def subscribe(self, calendar_id, person_id=None):
        calendar = Calendar.get_or_404(calendar_id)
        person = Person.get_or_404(person_id) if person_id else current_user
        try:
            subscription = PersonCalendarSub.create(
                person_id=person.id,
                calendar_id=calendar.id,
                meta={'color': Color.random()})
        except:
            abort(400, f'unable to subscribe to calendar {calendar_id}')
        return subscription, 201

    def unsubscribe(self, calendar_id, person_id=None):
        calendar = Calendar.get_or_404(calendar_id)
        person = Person.get_or_404(person_id) if person_id else current_user
        sub = db.session.query(PersonCalendarSub).filter(
            PersonCalendarSub.person_id == person.id,
            PersonCalendarSub.calendar_id == calendar.id
        ).first()
        if not sub:
            abort(
                400, f'person {person.id} not subscribed to calendar {calendar_id}')
        sub.delete()
        return True

    def update_subscription(self, calendar_id, **kwargs):
        subscriptions = current_user.calendar_subscriptions
        subscription = None
        for sub in subscriptions:
            if sub.calendar_id == calendar_id:
                subscription = sub
        if not subscription:
            abort(HTTPStatus.NOT_FOUND,
                  f'unable to find current subscription for calendar {calendar_id}')
        changed = False
        meta = copy.deepcopy(subscription.meta)
        for k, v in kwargs.items():
            if k not in meta or meta[k] != v:
                meta[k] = v
                changed = True
        if not changed:
            return abort(HTTPStatus.NOT_MODIFIED, 'no changes made')
        subscription.meta = meta
        subscription.save(refresh=True)
        return subscription

"""Person Controller."""

import json

from flask import abort
from flask import current_app
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import current_user
from sqlalchemy import or_
from http import HTTPStatus

from src.webserver.database import db
from ..models import Person
from ..models.person import PersonRole
from ..models import Calendar
from ..models.join import PersonCalendarSub
from ..models.join import PersonEventSub
from ._util import Color
from ._util import hash_password

IMAGE_MIME_TYPES = {
    'image/jpeg',
    'image/png'
}


class PersonController:
    """PersonController Class."""

    def get_config(self):
        if not current_user:
            return {}
        # event_subs = {
        #     sub.event_id: sub for sub in current_user.event_subscriptions}
        subs = {}
        for sub in current_user.calendar_subscriptions:
            person = sub.calendar.owner
            subs[person.id] = {
                'id': person.id,
                'handle': person.handle,
                'asset': person.format_asset(),
                'color': sub.meta['color']
            }
        return {
            'user': current_user._dict(),
            'subs': subs
        }

    def get(self, person_id=None):
        """Return user information."""
        if person_id:
            person = db.session.query(Person).filter(
                Person.id == person_id, Person.active == True).first()
            if not person:
                abort(HTTPStatus.NOT_FOUND,
                      f'user with id {person_id} does not exist')
            return person
        people = db.session.query(Person).filter(Person.active == True).all()
        return list(people)

    def create(self, name, password, email, username=None, allow_streaming=True):
        prefix, suffix = email.strip().split('@', 1)
        prefix = prefix.lower().replace(".", "")
        email = f'{prefix}@{suffix}'
        if not username:
            username = prefix
        username = username.strip()
        person = db.session.query(Person).filter(
            or_(Person.email.ilike(email),
                Person.handle.ilike(username))).first()
        if person:
            parts = []
            if person.email == email:
                parts.append(f'email {email}')
            if person.handle.lower() == username.lower():
                parts.append(f'username {username}')
            abort(HTTPStatus.CONFLICT,
                  f'user with {" and ".join(parts)} already exists')
        hashed_password = hash_password(password)
        if not username:
            username = email.split('@')[0]

        person = Person(
            name=name.strip(),
            password=hashed_password,
            email=email,
            handle=username
        )
        db.session.add(person)
        db.session.commit()
        db.session.refresh(person)
        calendar = Calendar(person.id)
        db.session.add(calendar)
        db.session.commit()
        return person, HTTPStatus.CREATED

    def delete(self, person_id):
        person = Person.get_or_404(person_id)
        person.update(active=False)
        return person

    def update(self, person_id, **kwargs):
        person = Person.get_or_404(person_id)
        changed = False
        for k, v in kwargs.items():
            if not hasattr(person, k):
                abort(HTTPStatus.BAD_REQUEST, f'unknown key: "{k}"')
            current_value = getattr(person, k)
            if k != current_value:
                setattr(person, k, v)
                changed = True
        if not changed:
            return abort(HTTPStatus.NOT_MODIFIED, 'no changes made')
        return person

    def subscribe(self, entity_id, entity_type, action):
        if entity_type not in ['calendar', 'event']:
            abort(HTTPStatus.BAD_REQUEST,
                  f'invalid entity_type [{entity_type}]')
        person = Person.get_or_404(entity_id)
        if entity_type == 'calendar':
            subscriptions = [
                cal.calendar_id for cal in person.calendar_subscriptions]
            sub = PersonCalendarSub.create(person_id=current_user.id,
                                           calendar_id=entity_id,
                                           meta={'color': Color.random()})
        elif entity_type == 'event':
            pass

        person.save()
        return person, HTTPStatus.CREATED

    def set_asset(self, person_id, file=None):
        person = Person.get_or_404(person_id)
        if file:
            mime_types = set(file.content_type.split(','))
            is_mime_type_allowed = any(
                mime_types.intersection(IMAGE_MIME_TYPES))

            if not is_mime_type_allowed:
                abort(HTTPStatus.BAD_REQUEST,
                      f'only files of type {IMAGE_MIME_TYPES} supported')
        person.asset = file
        person.save(refresh=True)
        return person

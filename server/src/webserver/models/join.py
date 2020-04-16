# coding=utf-8

"""Person model."""
import enum

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import BaseModel
from .helpers import JsonType


class PersonCalendarSub(BaseModel):

    __tablename__ = 'person_calendar_sub'
    __user_editable__ = [
        'meta'
    ]

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    calendar_id = Column(Integer, ForeignKey('calendar.id'))
    meta = Column(JsonType)
    created = Column(DateTime, server_default=func.now())

    person = relationship('Person', back_populates='calendar_subscriptions')
    calendar = relationship('Calendar', back_populates='subscribers')

    UniqueConstraint('person_id', 'calendar_id',
                     name='person_calendar_sub_uix0')

    def __init__(self, person_id, calendar_id, meta={}):
        """Inilaize the class."""
        self.person_id = person_id
        self.calendar_id = calendar_id
        self.meta = meta

    def __repr__(self):
        """String repr."""
        return f'<PersonCalendarSub id={self.id} person_id={self.person_id} calendar_id={self.calendar_id}>'

    def _dict(self):
        """Dictionary serialization."""
        return {
            'person_id': self.person_id,
            'calendar_id': self.calendar_id,
            'meta': self.meta
        }


class PersonEventSub(BaseModel):

    __tablename__ = 'person_event_sub'
    __user_editable__ = [
        'meta'
    ]

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    event_id = Column(Integer, ForeignKey('event.id'))
    meta = Column(JsonType)
    created = Column(DateTime, server_default=func.now())

    person = relationship('Person', back_populates='event_subscriptions')
    event = relationship('Event', back_populates='subscribers')

    UniqueConstraint('person_id', 'event_id', name='person_event_sub_uix0')

    def __init__(self, person_id, event_id, meta={}):
        """Inilaize the class."""
        self.person_id = person_id
        self.event_id = event_id
        self.meta = meta

    def __repr__(self):
        """String repr."""
        return f'<PersonEventSub id={self.id} person_id={self.person_id} event_id={self.calendar_id}>'

    def _dict(self):
        """Dictionary serialization."""
        return {
            'person_id': self.person_id,
            'event_id': self.event_id,
            'meta': self.meta
        }


class PersonEventQueue(BaseModel):

    __tablename__ = 'person_event_queue'
    __user_editable__ = [
        'meta'
    ]

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    event_id = Column(Integer, ForeignKey('event.id'))
    meta = Column(JsonType)
    created = Column(DateTime, server_default=func.now())

    UniqueConstraint('person_id', 'event_id', name='person_event_queue_uix0')

    def __init__(self, person_id, event_id):
        """Inilaize the class."""
        self.person_id = person_id
        self.event_id = event_id

    def __repr__(self):
        """String repr."""
        return f'<PersonEventQueue id={self.id} person_id={self.person_id} event_id={self.calendar_id}>'

    def _dict(self):
        """Dictionary serialization."""
        return {
            'person_id': self.person_id,
            'event_id': self.event_id
        }


class PersonGroup(BaseModel):

    __tablename__ = 'person_group'
    __user_editable__ = [
        'meta'
    ]

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    group_id = Column(Integer, ForeignKey('group.id'))
    meta = Column(JsonType)
    created = Column(DateTime, server_default=func.now())

    UniqueConstraint('person_id', 'group_id', name='person_group_uix0')

    person = relationship('Person', back_populates='groups')
    group = relationship('Group', back_populates='members')

    def __init__(self, person_id, group_id):
        """Inilaize the class."""
        self.person_id = person_id
        self.group_id = group_id

    def __repr__(self):
        """String repr."""
        return f'<PersonGroup id={self.id} person_id={self.person_id} group_id={self.calendar_id}>'

    def _dict(self):
        """Dictionary serialization."""
        return {
            'person_id': self.person_id,
            'group_id': self.group_id
        }

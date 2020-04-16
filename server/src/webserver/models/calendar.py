# coding=utf-8

"""Event model."""

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import BaseModel
from .helpers import JsonType


class Calendar(BaseModel):

    __tablename__ = 'calendar'
    __user_editable__ = [
        'private',
        'meta'
    ]

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    private = Column(Boolean, default=False)
    created = Column(DateTime, server_default=func.now())
    last_modified = Column(DateTime, server_default=func.now())
    meta = Column(JsonType)

    owner = relationship('Person', back_populates='calendar', uselist=False)
    events = relationship('Event', back_populates='calendar')

    subscribers = relationship(
        'PersonCalendarSub', back_populates='calendar')

    def __init__(self, owner_id, private=True):
        """Inilaize the class."""
        self.owner_id = owner_id
        self.private = private
        self.meta = {}

    def __repr__(self):
        """String repr."""
        return f'<Calendar id={self.id} owner_id={self.owner_id}>'

    def _dict(self):
        """Dictionary serialization."""
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'private': self.private,
            'created': self.created,
            'last_modified': self.last_modified
        }

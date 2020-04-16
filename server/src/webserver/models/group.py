# coding=utf-8

"""Block model."""

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from .base import BaseModel
from .helpers import JsonType


class Group(BaseModel):

    __tablename__ = 'group'
    __user_editable__ = [
        'name',
        'open',
        'slot_count',
        'meta'
    ]

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    name = Column(String(64))
    open = Column(Boolean, default=True)
    slot_count = Column(Integer)
    meta = Column(JsonType)

    event = relationship('Event', back_populates='groups')
    members = relationship('PersonGroup', back_populates='group')

    # queue = relationship('Person', back_populates='groups')

    def __init__(self, event_id, name, slot_count=1, open=True):
        """Inilaize the class."""
        self.event_id = event_id
        self.name = name
        self.slot_count = slot_count
        self.open = open
        self.meta = {}

    def __repr__(self):
        """String repr."""
        return f'<Group id={self.id} name={self.name}>'

    def _dict(self):
        """Dictionary serialization."""
        return {
            'id': self.id,
            'event_id': self.event_id,
            'name': self.name,
            'open': self.open,
            'slot_count': self.slot_count,
            'meta': self.meta
        }

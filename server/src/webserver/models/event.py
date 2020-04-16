# coding=utf-8

"""Event model."""

from depot.fields.filters.thumbnails import WithThumbnailFilter
from depot.fields.sqlalchemy import UploadedFileField
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import LargeBinary
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.webserver.depot import SPLASH_DEPOT

from .base import BaseModel
from .helpers import JsonType


class Event(BaseModel):

    SPLASH_SIZE = (540, 360)

    __tablename__ = 'event'
    __user_editable__ = [
        'title',
        'description',
        'start_time',
        'duration',
        'private',
        'meta'
    ]

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    description = Column(String(1024))
    calendar_id = Column(Integer, ForeignKey('calendar.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration = Column(Integer, nullable=False)
    private = Column(Boolean, default=False)
    created = Column(DateTime, server_default=func.now())
    last_modified = Column(DateTime, server_default=func.now())
    meta = Column(JsonType)

    asset = Column(UploadedFileField(
        upload_storage=SPLASH_DEPOT,
        filters=[
            WithThumbnailFilter(size=SPLASH_SIZE)
        ]
    ))

    calendar = relationship('Calendar', back_populates='events', uselist=False)
    groups = relationship('Group', back_populates='event')

    subscribers = relationship('PersonEventSub',
                               back_populates='event')

    def __init__(self, title, description, calendar_id, start_time, end_time, duration, private=True, meta={}):
        """Inilaize the class."""
        self.title = title
        self.description = description
        self.calendar_id = calendar_id
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.private = private
        self.meta = meta

    def format_asset(self):
        if self.asset:
            return self.asset.thumb_540x360_path

    def __repr__(self):
        """String repr."""
        return f'<Event id={self.id} title={self.title}>'

    def expanded(self):
        d = self._dict()
        d['owner'] = self.calendar.owner.simple_dict()
        d['groups'] = self.groups,
        d['slot_count'] = sum([g.slot_count for g in self.groups])
        return d

    def _dict(self):
        """Dictionary serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'calendar_id': self.calendar_id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'private': self.private,
            'asset': self.format_asset()
        }

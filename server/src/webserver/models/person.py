# coding=utf-8

"""Person model."""
import base64
import enum

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import LargeBinary
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from depot.fields.sqlalchemy import UploadedFileField
from depot.fields.filters.thumbnails import WithThumbnailFilter

from src.webserver.depot import AVATAR_DEPOT
from .base import BaseModel
from .helpers import JsonType
from .helpers import convert_asset


class PersonRole(enum.Enum):
    admin = 1
    moderator = 2
    plus = 3
    user = 4
    guest = 5


class Person(BaseModel):
    """Person class."""

    COVER_SIZE_SMALL = (64, 64)
    COVER_SIZE_MEDIUM = (256, 256)

    __tablename__ = 'person'
    __person_editable__ = ['name',
                           'email',
                           'password',
                           'allow_streaming',
                           'meta']

    id = Column(Integer, primary_key=True)
    name = Column('name', String(64),
                  nullable=False, unique=True)
    handle = Column('handle', String(16), nullable=False)
    email = Column('email', String(64), nullable=False)
    password = Column('password', String(256), nullable=False)
    active = Column('active', Boolean, default=True)
    public = Column('public', Boolean, default=True)
    role = Column('role', Enum(PersonRole))
    created = Column(DateTime, server_default=func.now())
    last_modified = Column(DateTime, server_default=func.now())
    meta = Column(JsonType)

    asset = Column(UploadedFileField(
        upload_storage=AVATAR_DEPOT,
        filters=[
            WithThumbnailFilter(size=COVER_SIZE_SMALL),
            WithThumbnailFilter(size=COVER_SIZE_MEDIUM)
        ]
    ))

    calendar = relationship('Calendar', back_populates='owner', uselist=False)

    calendar_subscriptions = relationship(
        'PersonCalendarSub', back_populates='person')
    event_subscriptions = relationship(
        'PersonEventSub', back_populates='person')
    groups = relationship('PersonGroup', back_populates='person')

    def __init__(self, name: str, handle: str, email: str, password: str, role: PersonRole = PersonRole.user):
        """Inilaize the class."""
        self.name = name
        self.handle = handle
        self.email = email
        self.password = password
        self.role = role

    def check_role(self, role: str) -> bool:
        if not hasattr(PersonRole, role):
            raise AttributeError(f'PersonRole does not have attr {role}')
        return self.role.value >= getattr(PersonRole, role).value

    def format_asset(self):
        if self.asset:
            return {
                'small': self.asset.thumb_64x64_path,
                'medium': self.asset.thumb_256x256_path
            }

    def __repr__(self) -> str:
        """String repr."""
        return f'<Person id={self.id} name={self.name}>'

    def simple_dict(self):
        return {
            'id': self.id,
            'handle': self.handle,
            'asset': self.format_asset()
        }

    def _dict(self) -> dict:
        """Dictionary serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'handle': self.handle,
            'email': self.email,
            'password': self.password,
            'active': self.active,
            'public': self.public,
            'role': self.role.name,
            'created': self.created,
            'last_modified': self.last_modified,
            'meta': self.meta,
            'asset': self.format_asset()
        }

# coding=utf-8

"""Asset model."""

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.sql import func

from .base import BaseModel
from .helpers import JsonType


class Asset(BaseModel):

    __tablename__ = 'calendar'
    __user_editable__ = []

    hash = Column(String(128), primary_key=True)
    path = Column(String(128))
    created = Column(DateTime, server_default=func.now())

    def __init__(self, hash, path):
        """Inilaize the class."""
        self.hash = hash
        self.path = path

    def __repr__(self):
        """String repr."""
        return f'<Asset hash={self.hash}>'

    def _dict(self):
        """Dictionary serialization."""
        return {
            'hash': self.hash,
            'path': self.path
        }

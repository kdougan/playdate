#!/usr/bin/python
# coding=utf-8

"""ChangeKey model."""

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .base import Base


class ChangeKey(Base):
    """ChangeKey class."""

    __tablename__ = 'change_key'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer)
    content_id = Column(Integer)
    content_type = Column(Integer)
    field = Column(String)
    old = Column('old_value', String)
    new = Column('new_value', String)

    def __init__(self, person_id, content_id, content_type,
                 field, old, new):
        """Inilaize the class."""
        self.person_id = person_id
        self.content_id = content_id
        self.content_type = content_type
        self.field = field
        self.old = old
        self.new = new

    def __repr__(self):
        """String repr."""
        return f'<ChangeKey id={self.id} field={self.field}>'

    def _dict(self):
        """Dictionary serialization."""
        return {
            'id': self.id,
            'person_id': self.person_id,
            'content_id': self.content_id,
            'content_type': self.content_type,
            'field': self.field,
            'old': self.old,
            'new': self.new
        }

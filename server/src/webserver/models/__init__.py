import uuid
from datetime import datetime

from flask_mongoengine import MongoEngine

db = MongoEngine()


def create_uuid():
    return str(uuid.uuid4).replace('-', '')


class Base(db.Document):
    created = db.DateTimeField(default=datetime.now)
    last_modified = db.DateTimeField(default=datetime.now)
    meta = {'abstract': True}

    def clean(self):
        self.last_modified = datetime.now()


class User(Base):
    name = db.StringField(required=True, max_length=64)
    username = db.StringField(required=True, max_length=16)
    email = db.StringField(required=True, max_length=64)
    password = db.StringField(required=True, max_length=256)
    allowStreaming = db.BooleanField(default=False)
    publicFields = db.ListField(db.StringField(max_length=16))
    active = db.BooleanField(default=True)
    hidden = db.BooleanField(default=False)
    meta = {'indexes': ['$username', 'active', 'hidden']}


class Group(Base):
    name = db.StringField(max_length=64)
    host = db.StringField(max_length=32)
    slotCount = db.IntField()
    slots = db.ListField(db.StringField(max_length=32))
    queue = db.ListField(db.StringField(max_length=32))


class Event(Base):
    title = db.StringField(required=True, max_length=64)
    description = db.StringField(max_length=256)
    owner = db.StringField(required=True, max_length=64)
    startTime = db.DateTimeField(required=True, default=datetime.now)
    endTime = db.DateTimeField(required=True, default=datetime.now)
    groups = db.ListField(db.StringField(max_length=32))

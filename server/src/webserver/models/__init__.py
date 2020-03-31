import uuid
from datetime import datetime

from flask_mongoengine import MongoEngine

db = MongoEngine()


def create_uuid():
    return str(uuid.uuid4).replace('-', '')


class Base(db.Document):
    created = db.DateTimeField(default=datetime.utcnow)
    last_modified = db.DateTimeField(default=datetime.utcnow)
    meta = {'abstract': True}

    def clean(self):
        self.last_modified = datetime.now()


class User(Base):
    name = db.StringField(required=True, max_length=64)
    _username = db.StringField(required=True, max_length=16, unique=True)
    username = db.StringField(required=True, max_length=16)
    email = db.StringField(required=True, max_length=64, unique=True)
    password = db.StringField(required=True, max_length=256)
    allow_streaming = db.BooleanField(default=False)
    public_fields = db.ListField(db.StringField(max_length=16))
    active = db.BooleanField(default=True)
    hidden = db.BooleanField(default=False)
    meta = {'indexes': ['$username', 'active', 'hidden']}

    @staticmethod
    def email_or_username(email, username):
        username = username.strip().lower()
        return User.objects(__raw__={'$or': [{'email': email}, {'_username': username}]})


class Group(Base):
    event_id = db.StringField(max_length=64)
    name = db.StringField(max_length=64)
    host = db.StringField(max_length=32)
    slot_count = db.IntField()
    slots = db.ListField(db.StringField(max_length=32))
    queue = db.ListField(db.StringField(max_length=32))


class Event(Base):
    title = db.StringField(required=True, max_length=64)
    description = db.StringField(max_length=256)
    owner = db.StringField(required=True, max_length=64)
    start_time = db.DateTimeField(required=True, default=datetime.utcnow)
    end_time = db.DateTimeField(required=True, default=datetime.utcnow)
    duration = db.IntField()
    groups = db.ListField(db.StringField(max_length=32))
    private = db.BooleanField(default=False)
    following = db.ListField(db.StringField(max_length=32))
    meta = {'indexes': ['$owner', 'start_time', 'end_time']}

    @staticmethod
    def time_range(start_time, end_time):
        return Event.objects(start_time__lt=end_time, end_time__gt=start_time)

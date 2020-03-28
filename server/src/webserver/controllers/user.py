"""Apple Pay Controller."""

import json

from flask import abort
from flask import current_app

from ..models import User
from . import hash_password
from . import verify_password


class UserController(object):
    """UserController Class."""

    def __init__(self):
        """Initialize the class."""
        pass

    def get(self, username=None):
        """Return user information."""
        if username:
            return json.loads(User.objects(username=username).first_or_404().to_json())
        users = User.objects(active__ne=False, hidden__ne=True)
        return [json.loads(user.to_json()) for user in users]

    def create(self, name, password, email, username=None, allow_streaming=True):
        email = email.lower().replace('.', '')
        user = User.objects(email=email).first()
        if user:
            abort(500, f'user with email {email} already exists')
        hashed_password = hash_password(password)
        if not username:
            username = email.split('@')[0]
        user = User(
            name=name,
            password=hashed_password,
            email=email,
            username=username,
            publicFields=['username'])
        user.save()
        return json.loads(user.to_json())

    def delete(self, username):
        user = User.objects(username=username).first_or_404()
        user.active = False
        user.save()
        return json.loads(user.to_json())

    def update(self, username, **kwargs):
        user = User.objects(username=username).first_or_404()
        changed = False
        for k, v in kwargs.items():
            if not hasattr(user, k):
                abort(400, f'unknown key: "{k}"')
            current_value = getattr(user, k)
            if k != current_value:
                setattr(user, k, v)
                changed = True
        if changed:
            user.save()
        return json.loads(user.to_json())

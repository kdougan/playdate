"""User Controller."""

import json

from flask import abort
from flask import current_app

from ..models import User
from . import hash_password


class UserController:
    """UserController Class."""

    def __init__(self):
        """Initialize the class."""
        pass

    def get(self, username=None):
        """Return user information."""
        if username:
            return json.loads(User.objects(username=username).first_or_404().to_json())
        users = User.objects(active__ne=False, hidden__ne=True)
        return list(map(lambda u: json.loads(u.to_json()), users))

    def create(self, name, password, email, username=None, allow_streaming=True):
        email = email.lower().replace('.', '').strip()
        if not username:
            username = email.split('@')[0]
        username = username.strip()
        _username = username.lower()
        user = User.email_or_username(email, username).first()
        if user:
            parts = []
            if user.email == email:
                parts.append(f'email {email}')
            if user._username == _username:
                parts.append(f'username {username}')
            abort(409, f'user with {" and ".join(parts)} already exists')
        hashed_password = hash_password(password)
        if not username:
            username = email.split('@')[0]
        user = User(
            name=name.strip(),
            password=hashed_password,
            email=email,
            username=username,
            _username=_username,
            public_fields=['username']
        )
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

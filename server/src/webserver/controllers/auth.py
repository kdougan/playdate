"""Event Controller."""

import json
import time
from datetime import datetime
from datetime import timedelta

from flask import abort
from flask import current_app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity

from ..models import User
from . import verify_password


class AuthController:
    """AuthController Class."""

    def __init__(self):
        """Initialize the class."""
        pass

    def authenticate(self, username, password):
        user = User.objects(_username=username.strip().lower()).first()
        if user and verify_password(password, user.password):
            access_token = create_access_token(
                identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(str(user.id))
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return abort(401, 'invalid credentials')

    def refresh(self):
        current_user = get_jwt_identity()
        return {
            'access_token': create_access_token(identity=current_user)
        }

"""Auth Controller."""

import json
import time
from datetime import datetime
from datetime import timedelta

from flask import abort
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity

from src.webserver.database import db
from ..models.person import Person
from ._util import verify_password


class AuthController:
    """AuthController Class."""

    def __init__(self):
        """Initialize the class."""
        pass

    @staticmethod
    def current_user_loader(person_id):
        return Person.get_by_id(person_id)

    def authenticate(self, email, password):
        person = db.session.query(Person).filter(
            Person.email.ilike(email)).first()
        if person and verify_password(password, person.password):
            access_token = create_access_token(
                identity=person.id, fresh=True)
            refresh_token = create_refresh_token(person.id)
            return {
                'id': person.id,
                'name': person.name,
                'email': person.email,
                'meta': person.meta,
                'token': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }
        return abort(401, 'invalid credentials')

    def refresh(self):
        current_user = get_jwt_identity()
        return {
            'access_token': create_access_token(identity=current_user)
        }

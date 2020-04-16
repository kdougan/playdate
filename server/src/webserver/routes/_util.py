from functools import wraps
from flask import abort
from flask_jwt_extended import get_jwt_identity

from ..models.person import PersonRole
from ..models.person import Person


def verify_access(role):
    def verify_access_outer(func):
        @wraps(func)
        def verify_access_inner(*args, **kwargs):
            user_id = get_jwt_identity()
            if not user_id:
                abort(403, 'no auth token present')
            current_user = Person.get_by_id(get_jwt_identity())
            if not current_user:
                abort(403, 'no user found')
            if not current_user.check_role(role):
                abort(403, 'current user not authorized')
            return func(*args, **kwargs)
        return verify_access_inner
    return verify_access_outer

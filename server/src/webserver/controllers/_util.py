import random

from flask import current_app
from passlib.hash import sha256_crypt
from werkzeug.security import safe_str_cmp


def hash_password(password):
    """Hash a password for storing."""
    secret_key = current_app.config.get('SECRET_KEY')
    return sha256_crypt.encrypt(password+secret_key)


def verify_password(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    secret_key = current_app.config.get('SECRET_KEY')
    return sha256_crypt.verify(provided_password+secret_key, stored_password)


class Color:
    red = '#f44336'
    pink = '#e91e63'
    purple = '#9c27b0'
    deep_purple = '#673ab7'
    indigo = '#3f51b5'
    blue = '#2196f3'
    light_blue = '#03a9f4'
    cyan = '#00bcd4'
    teal = '#009688'
    green = '#4caf50'
    light_green = '#8bc34a'
    lime = '#cddc39'
    yellow = '#ffeb3b'
    amber = '#ffc107'
    orange = '#ff9800'
    deep_orange = '#ff5722'
    brown = '#795548'
    gray = '#9e9e9e'
    blue_gray = '#607d8b'

    @classmethod
    def all(cls):
        return [cls.red,
                cls.pink,
                cls.purple,
                cls.deep_purple,
                cls.indigo,
                cls.blue,
                cls.light_blue,
                cls.cyan,
                cls.teal,
                cls.green,
                cls.light_green,
                cls.lime,
                cls.yellow,
                cls.amber,
                cls.orange,
                cls.deep_orange,
                cls.brown,
                cls.gray,
                cls.blue_gray]

    @classmethod
    def random(cls):
        return random.choice(cls.all())

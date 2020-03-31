import binascii
from passlib.hash import sha256_crypt
import os

from flask import current_app
from werkzeug.security import safe_str_cmp


def hash_password(password):
    """Hash a password for storing."""
    secret_key = current_app.config.get('SECRET_KEY')
    return sha256_crypt.encrypt(password+secret_key)


def verify_password(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    secret_key = current_app.config.get('SECRET_KEY')
    return sha256_crypt.verify(provided_password+secret_key, stored_password)

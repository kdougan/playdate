"""Application Configuration."""

import os
import re
import time

import dotenv
import redis

os.environ["NLS_LANG"] = ".UTF8"
os.environ['TZ'] = 'US/Pacific'
time.tzset()

path = os.path.dirname(__file__)
app_env = os.getenv('ENV')
local_dotenv = os.path.join(path, '.env')
env_dotenv = os.path.join(path, f'{app_env}.env')
base_dotenv = os.path.join(path, 'base.env')

de_vars = {'verbose': True}
if os.path.exists(local_dotenv):
    dotenv.load_dotenv(local_dotenv, **de_vars)
if os.path.exists(env_dotenv):
    dotenv.load_dotenv(env_dotenv, **de_vars)
dotenv.load_dotenv(base_dotenv, **de_vars)


def tobool(val):
    return str(val).lower() in ['true', '1', 't', 'y', 'yes', 'on']


class Config(dict):
    """Config class."""

    def __init__(self, defaults=None):
        """Init."""
        dict.__init__(self, defaults or {})

    def from_object(self, obj):
        """From object."""
        assert isinstance(obj, object)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)


class classproperty(property):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class BaseConfig(object):
    """Default configuration options."""

    _session_redis = None

    @classproperty
    def APP_NAME(self):
        return os.getenv('APP_NAME')

    @classproperty
    def SITE_NAME(self):
        return self.APP_NAME

    @classproperty
    def APP_ID(self):
        return os.getenv(
            'APP_ID', f'app.{self.SITE_NAME.lower().replace(" ", "-")}'
        )

    @classproperty
    def API_AUTH_KEY(self):
        return os.getenv('API_AUTH_KEY')

    @classproperty
    def SECRET_KEY(self):
        return os.getenv('SECRET_KEY')

    # @classproperty
    # def MAIL_SERVER(self):
    #     return os.getenv('MAIL_SERVER')

    # @classproperty
    # def MAIL_PORT(self):
    #     return int(os.getenv('MAIL_PORT'))

    @classproperty
    def REDIS_HOST(self):
        return os.getenv('REDIS_HOST')

    @classproperty
    def REDIS_PORT(self):
        return int(os.getenv('REDIS_PORT'))

    @classproperty
    def REDIS_URL(self):
        redis_url = f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'
        return os.getenv('REDIS_URL', redis_url)

    @classproperty
    def CACHE_TYPE(self):
        return os.getenv('CACHE_TYPE')

    @classproperty
    def CACHE_REDIS_URL(self):
        return os.getenv('CACHE_REDIS_URL', self.REDIS_URL)

    @classproperty
    def CACHE_DEFAULT_TIMEOUT(self):
        return int(os.getenv('CACHE_DEFAULT_TIMEOUT'))

    @classproperty
    def API_URL_PREFIX(self):
        return os.getenv('API_URL_PREFIX')

    @classproperty
    def SESSION_TYPE(self):
        return 'redis'

    @classproperty
    def SESSION_KEY_PREFIX(self):
        return os.getenv('SESSION_KEY_PREFIX')

    @classproperty
    def SESSION_REDIS(self):
        if not self._session_redis:
            self._session_redis = redis.StrictRedis.from_url(self.REDIS_URL)
        return self._session_redis

    @classproperty
    def PERMANENT_SESSION_LIFETIME(self):
        return int(os.getenv('PERMANENT_SESSION_LIFETIME'))

    @classproperty
    def MONGODB_USERNAME(self):
        return os.getenv('MONGODB_USERNAME')

    @classproperty
    def MONGODB_PASSWORD(self):
        return os.getenv('MONGODB_PASSWORD')

    @classproperty
    def MONGODB_HOST(self):
        return os.getenv('MONGODB_HOST')

    @classproperty
    def MONGODB_DB(self):
        return os.getenv('MONGODB_DB')

    @classproperty
    def MONGODB_SETTINGS(self):
        username = self.MONGODB_USERNAME
        password = self.MONGODB_PASSWORD
        host = self.MONGODB_HOST
        db = self.MONGODB_DB
        return {
            'db': 'irrelevant',
            'host': f'mongodb+srv://{username}:{password}@{host}/{db}?retryWrites=true&w=majority'
        }

    @classproperty
    def JWT_SECRET_KEY(self):
        return os.getenv('JWT_SECRET_KEY')


class DevConfig(BaseConfig):
    """Development configuration options."""

    DEVELOPMENT = True
    ASSETS_DEBUG = True
    WTF_CSRF_ENABLED = False


class TestConfig(BaseConfig):
    """Testing configuration options."""

    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = 'TEST'

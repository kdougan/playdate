from . import users
from . import events
from . import auth


def register(api):
    users.register(api)
    events.register(api)
    auth.register(api)

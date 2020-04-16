from . import people
from . import events
from . import auth
from . import admin
from . import calendars


def register(api):
    people.register(api)
    events.register(api)
    auth.register(api)
    admin.register(api)
    calendars.register(api)

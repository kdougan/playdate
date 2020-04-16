import pytest
from src.config import TestingConfig
from src.webserver import create_app
from src.webserver import db


@pytest.yield_fixture
def app():
    def _app(config_class):
        app = create_app(config_class)
        app.test_request_context().push()

        if config_class is TestingConfig:

            # always starting with an empty DB
            db.drop_all()
            from src.webserver.models import Person
            from src.webserver.models import Calendar
            from src.webserver.models import Event
            from src.webserver.models import Group
            from src.webserver.models import PersonCalendarSub
            from src.webserver.models import PersonEventSub
            from src.webserver.models import PersonEventQueue
            from src.webserver.models import PersonGroup

            db.create_all()

        return app

    yield _app
    db.session.remove()
    if str(db.engine.url) == TestingConfig.SQLALCHEMY_DATABASE_URI:
        db.drop_all()

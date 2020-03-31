"""Group Controller."""

import json
import time

from flask import abort
from flask import current_app

from ..models import Group
from . import hash_password
from . import verify_password


class GroupController:
    """GroupController Class."""

    def __init__(self):
        """Initialize the class."""
        pass

    def get(self, group_id):
        """Return Group information by id."""
        return json.loads(Group.objects(id=group_id).first_or_404().to_json())

    def create(self, event_id, host, slotCount, name=None):
        if not name:
            name = f'Group#{int(round(time.time() * 1000))}'
        group = Group(
            event_id=event_id,
            host=host,
            slotCount=slotCount,
            name=name
        )
        group.save()
        return json.loads(group.to_json())

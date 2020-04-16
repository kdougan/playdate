"""Group Controller."""

import json
import time

from ..models.group import Group


class GroupController:
    """GroupController Class."""

    def __init__(self):
        """Initialize the class."""
        pass

    def get(self, group_id):
        """Return Group information by id."""
        return Group.get_or_404(group_id)

    def create(self, event_id, name=None, slot_count=1, open=True, meta={}):
        if not name:
            name = f'Group#{int(round(time.time() * 1000))}'
        group = Group.create(
            event_id=event_id,
            name=name,
            slot_count=slot_count,
            open=open,
            meta=meta
        )
        return group, 201

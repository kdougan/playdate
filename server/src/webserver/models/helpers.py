"""Helper functions."""

import base64
import json
from PIL import Image
import io

from sqlalchemy import func
import sqlalchemy.types as types

from ..database import db


class JsonType(types.TypeDecorator):
    """JSON Type."""

    impl = types.Unicode

    def process_bind_param(self, value, engine):
        """Process Bind Param."""
        return json.dumps(value if value is not None else {})

    def process_result_value(self, value, engine):
        """Process Result Value."""
        if value:
            return json.loads(value)
        else:
            return {}


def max_(ident):
    """Max value for table/column."""
    return db.session.query(
        func.max(ident)
    ).scalar() or 0


def min_(ident):
    """Min value for table/column."""
    return db.session.query(
        func.min(ident)
    ).scalar() or 0


def convert_asset(asset):
    return base64.b64encode(Image.open(io.BytesIO(asset)).tobytes())

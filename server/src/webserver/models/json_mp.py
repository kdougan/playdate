"""Monkey patch to serialize object."""

from datetime import datetime
from json import JSONEncoder

from .base import Base


def _default(self, obj):
    if issubclass(type(obj), Base):
        return getattr(obj.__class__, "_dict", _default.default)(obj)
    if isinstance(obj, datetime):
        ts = int(obj.timestamp())
        return ts * 1000
    return str(obj)


_default.default = JSONEncoder.default  # Save unmodified default.
JSONEncoder.default = _default  # Replace it.

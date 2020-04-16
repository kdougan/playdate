# coding=utf-8

"""Base declaration."""

from sqlalchemy import MetaData
from flask_sqlalchemy import Model
from src.webserver.database import CRUDMixin

from sqlalchemy.ext.declarative import declarative_base


class Base(Model, CRUDMixin):
    """This class is a superclass of SA-generated Base class.

    which in turn is the superclass of all db-aware classes
    so we can define common functions here
    """

    def __setattr__(self, name, value):
        """Override Set Attribute.

        Raise an exception if attempting to assign to
        an atribute of a "read-only" object.
        Transient attributes need to be prefixed with "_t_"
        """
        if (getattr(self, '__readonly__', False) and
                name != "_sa_instance_state" and
                not name.startswith("_t_")):
            raise ValueError(
                "Trying to assign to {} of a read-only object {}".format(
                    name, self))
        super().__setattr__(name, value)


BaseModel = declarative_base(metadata=MetaData(schema='playdate'), cls=Base)

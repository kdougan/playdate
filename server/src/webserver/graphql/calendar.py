from graphene import Boolean
from graphene import DateTime
from graphene import ID
from graphene import Int
from graphene import JSONString
from graphene import ObjectType
from graphene import String
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import Calendar as CalendarModel
from ._util import Meta


class CalendarAttribute:
    pk = Int(source='id', description='ID of the calendar.')
    owner_id = String(description='Owner ID of the calendar.')
    private = Boolean(description='Calendar is private.')
    created = DateTime(description='Created date of the calendar.')
    meta = Meta(description='Meta object of the calendar.')


class Calendar(SQLAlchemyObjectType, CalendarAttribute):
    class Meta:
        model = CalendarModel
        interfaces = (relay.Node,)


class CalendarQuery(ObjectType):
    node = relay.Node.Field()

    celendar = relay.Node.Field(Calendar)
    calendars = SQLAlchemyConnectionField(Calendar)

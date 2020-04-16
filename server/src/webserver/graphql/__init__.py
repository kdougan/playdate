from graphene import ObjectType
from graphene import Schema
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene_sqlalchemy import SQLAlchemyObjectType

from .calendar import CalendarQuery
from .person import PersonQuery
from .event import EventQuery
from .group import GroupQuery


class Query(CalendarQuery,
            PersonQuery,
            EventQuery,
            GroupQuery,
            ObjectType):
    node = relay.Node.Field()


schema = Schema(query=Query)

from graphene import ID
from graphene import Boolean
from graphene import Int
from graphene import JSONString
from graphene import ObjectType
from graphene import String
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import Group as GroupModel
from ._util import Meta


class GroupAttribute:
    pk = Int(source='id', description='ID of the group.')
    event_id = Int(description='Event ID of the group')
    name = String(description='Name of the group')
    open = Boolean(description='Group is open')
    slot_count = Int(description='Slot count of the group')
    meta = Meta(description='Meta object of the group')


class Group(SQLAlchemyObjectType, GroupAttribute):
    class Meta:
        model = GroupModel
        interfaces = (relay.Node,)


class GroupQuery(ObjectType):
    node = relay.Node.Field()

    group = relay.Node.Field(Group)
    groups = SQLAlchemyConnectionField(Group)

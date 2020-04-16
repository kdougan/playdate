from graphene import Int
from graphene import DateTime
from graphene import JSONString
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType

from ._util import Meta

from ..models import PersonCalendarSub as PersonCalendarSubModel
from ..models import PersonEventSub as PersonEventSubModel
from ..models import PersonEventQueue as PersonEventQueueModel
from ..models import PersonGroup as PersonGroupModel


class PersonCalendarSubAttribute:
    person_id = Int(
        description='Person ID of the person\'s calendar subscription')
    calendar_id = Int(
        description='Calendar ID of the person\'s calendar subscription')
    meta = Meta(
        description='Meta object of the person\'s calendar subscription')


class PersonCalendarSub(SQLAlchemyObjectType, PersonCalendarSubAttribute):
    class Meta:
        model = PersonCalendarSubModel
        interfaces = (relay.Node,)


class PersonEventSubAttribute:
    person_id = Int(
        description='Person ID of the person\'s event subscription')
    event_id = Int(
        description='Event ID of the person\'s event subscription')
    meta = Meta(
        description='Meta object of the person\'s event subscription')


class PersonEventSub(SQLAlchemyObjectType, PersonEventSubAttribute):
    class Meta:
        model = PersonEventSubModel
        interfaces = (relay.Node,)


class PersonEventQueueAttribute:
    person_id = Int(description='Person ID of the person\'s queue entry.')
    event_id = Int(description='Event ID of the person\'s queue entry.')
    meta = Meta(description='Meta object of the person\'s queue entry.')
    created = DateTime(
        description='Created date of the person\'s queue entry.')


class PersonEventQueue(SQLAlchemyObjectType, PersonEventQueueAttribute):
    class Meta:
        model = PersonEventQueueModel
        interfaces = (relay.Node,)


class PersonGroupAttribute:
    person_id = Int(description='Person ID of the person\'s group entry.')
    group_id = Int(description='Group ID of the person\'s group entry.')
    meta = Meta(description='Meta object of the person\'s group entry.')
    created = DateTime(
        description='Created date of the person\'s group entry.')


class PersonGroup(SQLAlchemyObjectType, PersonGroupAttribute):
    class Meta:
        model = PersonGroupModel
        interfaces = (relay.Node,)

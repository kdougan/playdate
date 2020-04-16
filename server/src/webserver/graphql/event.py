from graphene import Boolean
from graphene import DateTime
from graphene import Field
from graphene import ID
from graphene import Int
from graphene import JSONString
from graphene import ObjectType
from graphene import String
from graphene import List
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import or_

from ..models import Event as EventModel
from .person import Person
from .person import PersonModel
from .joins import PersonCalendarSub
from .joins import PersonCalendarSubModel
from .joins import PersonEventSub
from .joins import PersonEventSubModel
from ._util import Asset
from ._util import Meta


class EventAttribute:
    pk = Int(source='id', description='ID of the event.')
    title = String(description='Title of the event.')
    description = String(description='Description of the event.')
    calendar_id = Int(description='Calendar ID of the event.')
    start_time = DateTime(description='Start time of the event.')
    end_time = DateTime(description='End time of the event.')
    duration = Int(description='Duration of the event.')
    private = Boolean(description='Event is private.')
    asset = Asset(description="Asset (Splash) of the event.")
    meta = Meta(description='Meta object of the event.')


class Event(SQLAlchemyObjectType, EventAttribute):
    class Meta:
        model = EventModel
        interfaces = (relay.Node,)


class EventQuery(ObjectType):
    node = relay.Node.Field()

    event = relay.Node.Field(Event)
    events = SQLAlchemyConnectionField(Event)

    event_for_pk = Field(Event, id=Int())

    def resolve_event_for_pk(self, info, id):
        query = Event.get_query(info)
        return query.filter(EventModel.id == id).first()

    event_range = Field(
        lambda: List(Event), start_time=DateTime(), end_time=DateTime())

    def resolve_event_range(self, info, start_time, end_time):
        query = Event.get_query(info)
        return query.filter(or_(
            EventModel.start_time <= end_time,
            EventModel.end_time >= start_time
        )).all()

    event_range_for_person = Field(
        lambda: List(Event), start_time=DateTime(), end_time=DateTime(), person_id=Int())

    def resolve_event_range_for_person(self, info, start_time, end_time, person_id):
        person = Person.get_query(info).filter(
            PersonModel.id == person_id).first()
        print(f'+++ person calendar id: {person.calendar.id} +++')
        calendar_subscriptions = PersonCalendarSub.get_query(
            info
        ).filter(
            PersonCalendarSubModel.person_id == person_id
        ).all()
        calendar_ids = [sub.calendar_id for sub in calendar_subscriptions]
        event_subscriptions = PersonEventSub.get_query(
            info
        ).filter(
            PersonEventSubModel.person_id == person_id
        ).all()
        event_ids = [sub.event_id for sub in event_subscriptions]
        query = Event.get_query(info)
        events = query.filter(
            or_(EventModel.start_time <= end_time,
                EventModel.end_time >= start_time),
            or_(EventModel.calendar_id == person.calendar.id,
                EventModel.calendar_id.in_(calendar_ids),
                EventModel.id.in_(event_ids))
        ).all()
        return events

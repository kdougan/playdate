from graphene import ID
from graphene import Int
from graphene import Boolean
from graphene import DateTime
from graphene import JSONString
from graphene import ObjectType
from graphene import Schema
from graphene import String
from graphene import relay
from graphene import Field
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import Person as PersonModel
from .joins import PersonCalendarSub
from .joins import PersonEventQueue
from .joins import PersonEventSub

from ._util import Asset
from ._util import Meta


class PersonAttribute:
    pk = Int(source='id', description='ID of the person.')
    name = String(description='Name of the person.')
    handle = String(description='Handle of the person.')
    email = String(description='Email of the person.')
    active = Boolean(description='Person is active.')
    public = Boolean(description='Person is public.')
    role = String(description='Role of the person.')
    created = DateTime(description='Creation date of the person.')
    meta = Meta(description='Meta object of the person.')
    asset = Asset(description='Asset (Avatar) of the person.')


class Person(SQLAlchemyObjectType, PersonAttribute):
    class Meta:
        model = PersonModel
        filter_fields = ['id', 'handle', 'email']
        interfaces = (relay.Node,)


class PersonQuery(ObjectType):
    node = relay.Node.Field()

    person = relay.Node.Field(Person)
    people = SQLAlchemyConnectionField(Person)

    person_by_pk = Field(Person, id=Int())
    person_by_email = Field(Person, email=String())

    def resolve_person_by_pk(self, info, id):
        query = Person.get_query(info)
        return query.filter(PersonModel.id == id).first()

    def resolve_person_by_email(self, info, email):
        query = Person.get_query(info)
        return query.filter(PersonModel.email == email).first()

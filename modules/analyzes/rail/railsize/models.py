import datetime

from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import ObjectIdField
from mongoengine import IntField
from mongoengine import ReferenceField

from modules.organization.models import Organization


class RailSize(Document):
    _created_date = DateTimeField(default=datetime.datetime.now)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.now)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()

    _key_organization = ReferenceField(Organization, required=True, reverse_delete_rule=2)

    railtext = StringField(required=True)
    sizerownumber = IntField(required=True)
    rail_length = IntField(required=True)
    rail_width = IntField(required=True)
    rail_height = IntField(required=True)

    rail_flans_length = IntField(required=True)
    rail_flans_width = IntField(required=True)
    rail_flans_height = IntField(required=True)

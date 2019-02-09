import datetime

from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import ObjectIdField
from mongoengine import ReferenceField

from modules.organization.models import Organization

class Volume(Document):
    _created_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()

    _key_organization = ReferenceField(Organization, required=True, reverse_delete_rule=2)
    volume = StringField(required=True)

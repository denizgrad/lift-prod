import datetime

from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import ObjectIdField
from mongoengine import DecimalField
from mongoengine import ReferenceField

from modules.analyzes.console.consoletype.models import ConsoleType
from modules.organization.models import Organization


class Console(Document):

    _created_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()
    analysis_date = StringField(required=True)
    console_name = StringField(required=True)
    _key_console_type = ReferenceField(ConsoleType, required=True, reverse_delete_rule=3)
    _key_organization = ReferenceField(Organization, required=True, reverse_delete_rule=2)
    unit_price = DecimalField(required=True)
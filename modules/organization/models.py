import datetime
from mongoengine import ObjectIdField, BooleanField
from mongoengine import ReferenceField
from mongoengine import Document
from mongoengine import IntField
from mongoengine import FloatField
from mongoengine import ListField
from mongoengine import StringField
from mongoengine import DateTimeField

from modules.currency.models import Currency


class Organization(Document):
    _created_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()

    _key_currency = ReferenceField(Currency, required=False, reverse_delete_rule=3)

    is_enabled = BooleanField(default=True)
    name = StringField(required=True)
    type = IntField(required=True)
    city = StringField()
    working_days = ListField(IntField(min_value=0, max_value=6))
    work_starts_at = FloatField(min_value=0.00, max_value=23.30)
    work_ends_at = FloatField(min_value=0.00, max_value=23.30)
    created_date = DateTimeField(default=datetime.datetime.utcnow)
    created_by = StringField()
    updated_by = StringField()


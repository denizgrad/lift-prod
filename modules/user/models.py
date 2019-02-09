import datetime

from mongoengine import (Document, StringField, ListField, BinaryField,
                         BooleanField, ReferenceField, DateTimeField)
from modules.organization.models import Organization


class User(Document):
    email = StringField(required=True)
    full_name = StringField()
    first_name = StringField()
    last_name = StringField()
    phone = StringField()
    roles = ListField(StringField())
    password = StringField()
    is_enabled = BooleanField()
    public_commenter = BooleanField()
    admin = BooleanField()
    self_register = BooleanField()
    role = StringField()
    organization = ReferenceField(Organization, required=True, reverse_delete_rule=2)
    created_date = DateTimeField(default=datetime.datetime.utcnow)
    created_by = StringField()
    updated_by = StringField()

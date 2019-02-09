import datetime

from mongoengine import (Document, StringField, ReferenceField, DateTimeField, ListField)
from modules.organization.models import Organization


class Permission (Document):
    module_name = StringField(required=True)
    action_list = ListField(StringField(), required=True)
    role_name = StringField(required=True)
    organization = ReferenceField(Organization, required=True, reverse_delete_rule=2)
    created_date = DateTimeField(default=datetime.datetime.utcnow)
    created_by = StringField()
    updated_by = StringField()

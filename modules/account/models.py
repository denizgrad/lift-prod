import datetime
from modules.organization.models import Organization
from mongoengine import (
    Document,
    EmailField,
    StringField,
    DateTimeField,
    ReferenceField,
)


class Accounts(Document):
    _created_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_created_user = ReferenceField('User')
    _last_modified_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_last_modified_user = ReferenceField('User')
    _key_owner_user = ReferenceField('User')

    _key_organization = ReferenceField(Organization, required=True, reverse_delete_rule=2)

    code = StringField(required=True, unique_with=['_key_organization'])
    name = StringField(required=True, unique_with=['_key_organization'])
    # vergi dairesi
    tax_administration = StringField()
    # vergi numarası
    tax_id_number = StringField()
    web_address = StringField()
    phone = StringField()
    email = EmailField()

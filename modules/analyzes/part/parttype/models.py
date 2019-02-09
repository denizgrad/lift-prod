import datetime

from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import DecimalField
from mongoengine import ObjectIdField
from mongoengine import ReferenceField

from modules.currency.models import Currency
from modules.organization.models import Organization


class PartType(Document):
    _created_date = DateTimeField(default=datetime.datetime.now)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.now)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()

    _key_organization = ReferenceField(Organization, required=True, reverse_delete_rule=2)
    _key_kur_cinsi = ReferenceField(Currency, required=True, reverse_delete_rule=3)

    name = StringField(required=True)
    price_local = DecimalField(required=True)
    price_global = DecimalField(required=True)


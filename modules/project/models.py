import datetime

from abstracts import AbstractDocument
from modules.account import Accounts
from modules.currency.models import Currency
from modules.user.models import User
from modules.organization.models import Organization
from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    ReferenceField,
    FloatField
)


class Project(AbstractDocument):
    # _created_date = DateTimeField(default=datetime.datetime.utcnow)
    # _key_created_user = ReferenceField(User)
    # _last_modified_date = DateTimeField(default=datetime.datetime.utcnow)
    # _key_last_modified_user = ReferenceField(User)
    # _key_owner_user = ReferenceField(User)
    # _key_organization = ReferenceField(Organization, required=True, reverse_delete_rule=2)

    status = StringField(required=True)
    _key_account_owner = ReferenceField(Accounts, required=True, reverse_delete_rule=3)
    _key_account_contractor = ReferenceField(Accounts, required=True, reverse_delete_rule=3)
    name = StringField(required=True)
    amount = FloatField()
    lift_total = FloatField()
    _key_currency_amount = ReferenceField(Currency, required=True, reverse_delete_rule=3)
    _key_currency_lift_total = ReferenceField(Currency, required=True, reverse_delete_rule=3)
    bid_date = DateTimeField()
    start_date = DateTimeField()
    mounting_start_date = DateTimeField()

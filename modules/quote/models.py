import datetime

from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import ReferenceField
from mongoengine import FloatField

from modules.currency.models import Currency
from modules.user.models import User
from modules.account.models import Accounts
from modules.project.models import Project
from modules.organization.models import Organization


class Quote(Document):
    _created_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_created_user = ReferenceField(User)
    _last_modified_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_last_modified_user = ReferenceField(User)
    _key_owner_user = ReferenceField(User)
    _key_organization = ReferenceField(Organization, required=True, reverse_delete_rule=2)

    _key_account = ReferenceField(Accounts, required=True, reverse_delete_rule=3)
    _key_project = ReferenceField(Project, required=True, reverse_delete_rule=3)
    expiry_date = DateTimeField(required=True)
    amount_total = FloatField(required=True)
    _key_currency_amount_total = ReferenceField(Currency, required=True, reverse_delete_rule=3)

    #_ANALIZ CHILDREN


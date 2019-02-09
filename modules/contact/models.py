from abstracts import AbstractDocument
from modules.account.models import Accounts
from mongoengine import (
    StringField,
    ReferenceField,
    DENY
)


class Contact(AbstractDocument):
    _key_account = ReferenceField(Accounts, required=True, reverse_delete_rule=DENY)

    code = StringField()
    name = StringField(required=True)
    surname = StringField()
    full_name = StringField()
    info = StringField()
    phone = StringField()
    mobile = StringField()
    email = StringField()
    fax = StringField()

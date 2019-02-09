import datetime

from mongoengine import DateTimeField, ObjectIdField
from mongoengine import Document
from mongoengine import ReferenceField
from mongoengine import StringField

from modules.contact.models import Contact
from modules.organization.models import Organization


class ContactItem(Document):
    _created_date = DateTimeField(default=datetime.datetime.now)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.now)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()

    _key_organization = ReferenceField(Organization, required=True)
    _key_contact = ReferenceField(Contact, required=True, reverse_delete_rule=3)

    code = StringField(required=True)
    info = StringField()
    phone_no = StringField()
    mobile_no = StringField()
    email = StringField()
    fax = StringField()

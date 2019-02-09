import datetime

from mongoengine import Document, StringField, DictField, ReferenceField, ListField, DateTimeField, IntField

from modules.helper2 import helper
from resources import db
from ..user.models import User


class Notification(Document):
    """
    Records for showing in-app notification
    """
    message = StringField()
    message_body = DictField()
    created_by = ReferenceField(User)
    reads_by = ListField(StringField())
    related_to = ReferenceField(User)
    created_date = DateTimeField(default=datetime.datetime.utcnow)
    message_no = IntField(default=1)

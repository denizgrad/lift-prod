import datetime

from flask_login import current_user
from mongoengine import Document, PointField, DateTimeField, ReferenceField, StringField

from modules.message.models import Message
from modules.photo.models import Photo

from modules.user.models import User


class Location(Document):
    location = PointField(required=True)
    created_date = DateTimeField(default=datetime.datetime.utcnow)
    created_by = ReferenceField(User)
    relation_desc = StringField(required=True)
    photo = ReferenceField(Photo)
    message = ReferenceField(Message)



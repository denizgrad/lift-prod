import datetime

import mongoengine
from bson import json_util
from mongoengine import (Document, IntField, DictField,
                         StringField, BooleanField, ReferenceField,
                         DateTimeField, ListField)
from mongoengine.errors import DoesNotExist
from flask_mongoengine import QuerySet
from modules.user.models import User
from resources import app
from ..organization.models import Organization


class CustomQuerySet(QuerySet):
    def to_json(self):
        query = []
        for doc in self:
            data = doc.to_json()
            if data:
                query.append(data)
        return "[%s]" % (",".join([q for q in query]))


class Message(Document):
    """
    Message records written by system or user
    If system type = 1
    If user type = 2
    """
    type = IntField(required=True)
    # oto message body for building up in front-end
    body = DictField()
    # user message body
    text_body = StringField()
    # if created after case accessed by qr
    qr = BooleanField()
    created_company = ReferenceField(Organization)
    created_date = DateTimeField(default=datetime.datetime.utcnow)
    created_by = ReferenceField(User)

    mentions = ListField(ReferenceField(User))
    related_to_field = StringField()
    # meta = {'allow_inheritance': True}

    meta = {'queryset_class': CustomQuerySet}
"""
Custom to_json method
    def to_json(self):
        data = self.to_mongo()
        try:
            if self.related_to_damage:
                oid = self.related_to_damage.id
                Vehicle = self.related_to_damage.vehicle.to_mongo()
                data["related_to_damage"] = {
                    "_id": {"$oid": oid},
                    "Vehicle": Vehicle
                }
        except mongoengine.errors.DoesNotExist as e:
            app.logger.exception(e)
        return json_util.dumps(data)
"""

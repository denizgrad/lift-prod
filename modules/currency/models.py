import datetime
from bson import ObjectId
from mongoengine import Document
from mongoengine import StringField
from mongoengine import SequenceField
from mongoengine import DateTimeField
from mongoengine import ReferenceField
from mongoengine import FloatField
from mongoengine import ObjectIdField


class Currency(Document):

    _created_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()


    code = StringField(required=True)
    name = StringField(required=True)


class Parity(Document):
    _created_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()

    _key_organization = ObjectIdField()
    _key_currency = ReferenceField(Currency, required=True)
    _key_currency_organization = ReferenceField(Currency)

    bid_price = FloatField(required=True)
    ask_price = FloatField(required=True)

    @staticmethod
    def get_parity_by_currency(currency_id):
        return Parity.objects(_key_currency=ObjectId(currency_id)).order_by('-id').first()

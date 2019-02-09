import datetime

from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import ObjectIdField
from mongoengine import DecimalField
from mongoengine import ReferenceField

from modules.analyzes.cabin.cabintypes.models import CabinType
from modules.analyzes.machineEngine.models import EngineRoomType
from modules.analyzes.machineEngine.capacity.models import Capacity
from modules.organization.models import Organization


class Cabin(Document):

    _created_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()

    analysis_date = StringField(required=True)
    price = DecimalField(required=True)

    """joins"""
    _key_organization = ReferenceField(Organization, required=True,reverse_delete_rule=2)
    _key_cabin_type = ReferenceField(CabinType, required=True, reverse_delete_rule=3)
    _key_room_type = ReferenceField(EngineRoomType, required=True, reverse_delete_rule=3)
    _key_capacity = ReferenceField(Capacity, required=True, reverse_delete_rule=3)




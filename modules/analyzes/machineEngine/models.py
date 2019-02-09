import datetime

from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import ObjectIdField
from mongoengine import DecimalField
from mongoengine import ReferenceField

from modules.analyzes.machineEngine.roomtype.models import EngineRoomType
from modules.analyzes.machineEngine.enginespeed.models import EngineSpeed
from modules.analyzes.machineEngine.capacity.models import Capacity
from modules.analyzes.machineEngine.enginetype.models import EngineType
from modules.analyzes.machineEngine.volume.models import Volume
from modules.currency.models import Currency
from modules.discount.models import Discount
from modules.organization.models import Organization


class MachineEngine(Document):

    _created_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()
    analysis_date = StringField(required=True)

    _key_organization = ReferenceField(Organization, required=True, reverse_delete_rule=2)
    _key_room_type = ReferenceField(EngineRoomType, required=True, reverse_delete_rule=3)
    _key_engine_speed = ReferenceField(EngineSpeed, required=True, reverse_delete_rule=3)
    _key_volume = ReferenceField(Volume, required=True, reverse_delete_rule=3)
    _key_capacity = ReferenceField(Capacity, required=True, reverse_delete_rule=3)
    _key_engine_type = ReferenceField(EngineType, required=True, reverse_delete_rule=3)
    _key_kur_cinsi = ReferenceField(Currency, required=True, reverse_delete_rule=3)
    _key_iskonto = ReferenceField(Discount, required=True, reverse_delete_rule=3)

    birim_fiyat = DecimalField(required=True)

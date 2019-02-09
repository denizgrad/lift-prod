import datetime

from mongoengine import Document, ListField
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import ObjectIdField
from mongoengine import DecimalField
from mongoengine import ReferenceField

from modules.analyzes.door.paneltype.models import PanelType
from modules.analyzes.door.doortype.models import DoorType
from modules.analyzes.door.doorsize.models import DoorSize
from modules.organization.models import Organization

from modules.currency.models import Currency
from modules.brand.models import Brand
from modules.discount.models import Discount

class Door(Document):

    _created_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()
    analysis_date = StringField(required=True)

    _key_panel_type = ReferenceField(PanelType, required=True, reverse_delete_rule=3)
    _key_door_type = ReferenceField(DoorType, required=True, reverse_delete_rule=3)
    _key_brand = ReferenceField(Brand, required=True, reverse_delete_rule=3)
    _key_door_size_list = ListField(ReferenceField(DoorSize, required=True, reverse_delete_rule=3))
    _key_currency = ReferenceField(Currency, required=False, reverse_delete_rule=3)
    _key_discount = ReferenceField(Discount, required=True, reverse_delete_rule=3)
    _key_organization = ReferenceField(Organization, required=True, reverse_delete_rule=2)

    price = DecimalField(required=True)


import datetime

from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import ObjectIdField
from mongoengine import DecimalField
from mongoengine import ReferenceField

from modules.analyzes.machineEngine.models import EngineRoomType
from modules.brand.models import Brand
from modules.discount.models import Discount
from modules.organization.models import Organization
from modules.analyzes.controlPanel.controlpanelextra.models import ControlPanelExtra
from modules.analyzes.controlPanel.panelsize.models import ControlPanelSize
from modules.analyzes.controlPanel.controlpanelbuttontype.models import ControlPanelButtonType


class ControlPanel(Document):

    _created_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.utcnow)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()

    _key_brand = ReferenceField(Brand, required=True, reverse_delete_rule=3)
    _key_room_type = ReferenceField(EngineRoomType, required=True, reverse_delete_rule=3)
    _key_cp_size = ReferenceField(ControlPanelSize, required=True, reverse_delete_rule=3)
    _key_cp_button_type = ReferenceField(ControlPanelButtonType, required=True, reverse_delete_rule=3)
    _key_extra_type = ReferenceField(ControlPanelExtra, required=True, reverse_delete_rule=3)

    _key_organization = ReferenceField(Organization, required=True, reverse_delete_rule=2)
    _key_discount = ReferenceField(Discount, required=True, reverse_delete_rule=3)

    analysis_date = DateTimeField(default=datetime.datetime.utcnow)
    ready_installation = StringField(required=True)
    rfid_card = StringField(required=True)
    price = DecimalField(required=True)

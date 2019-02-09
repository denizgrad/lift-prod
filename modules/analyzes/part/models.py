import datetime

from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import ObjectIdField
from mongoengine import DecimalField
from mongoengine import ReferenceField

from modules.analyzes.part.parttype.models import PartType
from modules.currency.models import Currency
from modules.organization.models import Organization
from modules.analyzes.machineEngine.enginespeed.models import EngineSpeed


class Part(Document):

    _created_date = DateTimeField(default=datetime.datetime.now)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.now)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()

    analysis_date = DateTimeField(default=datetime.datetime.now)

    _key_organization = ReferenceField(Organization, required=True, reverse_delete_rule=2)
    _key_parts_type = ReferenceField(PartType, required=True, reverse_delete_rule=3)
    _key_regulator_speed_type = ReferenceField(EngineSpeed, required=True, reverse_delete_rule=3)
    _key_currency = ReferenceField(Currency, required=True, reverse_delete_rule=3)

    price = DecimalField(required=True)

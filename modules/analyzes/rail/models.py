import datetime

from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import ObjectIdField
from mongoengine import DecimalField
from mongoengine import ReferenceField

from modules.analyzes.rail.railsize.models import RailSize

from modules.currency.models import Currency
from modules.discount.models import Discount
from modules.brand.models import Brand
from modules.organization.models import Organization


class Rail(Document):
    _created_date = DateTimeField(default=datetime.datetime.now)
    _key_created_user = ObjectIdField()
    _last_modified_date = DateTimeField(default=datetime.datetime.now)
    _key_last_modified_user = ObjectIdField()
    _key_owner_user = ObjectIdField()

    analysis_date = DateTimeField(default=datetime.datetime.now)
    _key_organization = ReferenceField(Organization, required=True, reverse_delete_rule=2)
    _key_brand = ReferenceField(Brand, required=True, reverse_delete_rule=3)
    _key_kur_cinsi = ReferenceField(Currency, required=True, reverse_delete_rule=3)
    _key_iskonto = ReferenceField(Discount, required=True, reverse_delete_rule=3)

    _key_rail_size_1 = ReferenceField(RailSize, required=True, reverse_delete_rule=3)
    _key_rail_size_2 = ReferenceField(RailSize, reverse_delete_rule=1)
    _key_rail_size_3 = ReferenceField(RailSize, reverse_delete_rule=1)
    _key_rail_size_4 = ReferenceField(RailSize, reverse_delete_rule=1)
    _key_rail_size_5 = ReferenceField(RailSize, reverse_delete_rule=1)
    _key_rail_size_6 = ReferenceField(RailSize, reverse_delete_rule=1)
    _key_rail_size_7 = ReferenceField(RailSize, reverse_delete_rule=1)
    _key_rail_size_8 = ReferenceField(RailSize, reverse_delete_rule=1)

    _key_rail_flans_size_1 = ReferenceField(RailSize, required=True, reverse_delete_rule=3)
    _key_rail_flans_size_2 = ReferenceField(RailSize, reverse_delete_rule=1)
    _key_rail_flans_size_3 = ReferenceField(RailSize, reverse_delete_rule=1)
    _key_rail_flans_size_4 = ReferenceField(RailSize, reverse_delete_rule=1)
    _key_rail_flans_size_5 = ReferenceField(RailSize, reverse_delete_rule=1)
    _key_rail_flans_size_6 = ReferenceField(RailSize, reverse_delete_rule=1)
    _key_rail_flans_size_7 = ReferenceField(RailSize, reverse_delete_rule=1)
    _key_rail_flans_size_8 = ReferenceField(RailSize, reverse_delete_rule=1)

    birim_fiyat = DecimalField(required=True)


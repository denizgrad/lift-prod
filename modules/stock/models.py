from abstracts import AbstractDocument
from ..brand.models import Brand
from ..currency.models import Currency
from ..analysis_item.models import AnalysisItem
from ..analysis_category.models import AnalysisCategory
from .enum_types import EnumStockType, EnumUnitTypes, EnumMainUnitTypes
from mongoengine import (
    StringField,
    IntField,
    FloatField,
    ReferenceField,
    DictField,
    BooleanField,
    DENY
)


class Stock(AbstractDocument):

    # Stock Model References
    _key_currency = ReferenceField(Currency)
    _key_brand = ReferenceField(Brand, reverse_delete_rule=DENY)
    _key_category = ReferenceField(AnalysisCategory, reverse_delete_rule=DENY)
    _key_category_item = ReferenceField(AnalysisItem, reverse_delete_rule=DENY)

    barcode = StringField()
    stock_code = StringField(unique=True, required=True)
    name = StringField()
    description = StringField()
    model = StringField()  # Model / Özellik
    stock_type = StringField(default=EnumStockType.STOCK.value)
    unit_type = StringField(default=EnumUnitTypes.PIECE.value)
    main_unit_type = StringField(default=EnumMainUnitTypes.PIECE.value)
    vat_rate = IntField(default=18, min_value=0, max_value=100)
    low_stock_alarm = IntField(default=0)
    max_stock_alarm = IntField()
    unit_price = FloatField(default=0)
    quantity = FloatField(default=0)
    total_price = FloatField(default=0)
    buying_price = FloatField()
    list_price = FloatField()
    analysis_settings = DictField()
    use_analysis_settings = BooleanField(default=False)

    meta = {'indexes': [
        {
            'fields': ['$barcode', '$stock_code', '$name'],
            'default_language': 'turkish',
            'weights': {'title': 2, 'content': 2}
         }
    ]}


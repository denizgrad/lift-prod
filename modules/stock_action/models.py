from abstracts import AbstractDocument
from ..user.models import User
from ..stock.models import Stock
from ..currency.models import Currency, Parity
from .enum_types import EnumActionTypes
from mongoengine import (
    StringField,
    IntField,
    FloatField,
    DateTimeField,
    ReferenceField,
    BooleanField,
    DENY
)


class StockAction(AbstractDocument):
    # Stock Action References
    _key_stock = ReferenceField(Stock, reverse_delete_rule=DENY)
    _key_currency = ReferenceField(Currency)
    _key_parity = ReferenceField(Parity)
    # Safe Delete Fields
    _is_deleted = BooleanField()
    _delete_description = StringField()
    _deleted_date = DateTimeField()
    _deleted_user = ReferenceField(User)

    action_no = IntField(default=1)
    action_type = StringField(default=EnumActionTypes.GIRIS.value)  # İşlem Tipi [Giriş, Çıkış]
    description = StringField()
    waybill = IntField()  # İrsaliye
    quantity = FloatField(default=0)  # Miktar
    unit_price = FloatField(default=0)
    total_price = FloatField()
    parity_value = FloatField()

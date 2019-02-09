from abstracts import AbstractDocument
from ..analysis.models import Analysis
from ..stock.models import Stock
from ..brand.models import Brand
from mongoengine import (
    DENY,
    StringField,
    ReferenceField,
)

__all__ = ['AnalysisLineItems']


class AnalysisLineItems(AbstractDocument):

    _key_analysis = ReferenceField(Analysis, reverse_delete_rule=DENY)
    _key_stock = ReferenceField(Analysis, reverse_delete_rule=DENY)
    _key_brand = ReferenceField(Brand, reverse_delete_rule=DENY)
    name = StringField(required=True)
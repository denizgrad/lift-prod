from abstracts import AbstractDocument
from ..analysis_category.enum_types import EnumCategoryTypes
from mongoengine import StringField


class Brand(AbstractDocument):
    name = StringField(required=True, unique_with=['_key_organization'])
    description = StringField()
    analysis_category = StringField()

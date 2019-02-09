from abstracts import AbstractDocument
from .enum_types import EnumCategoryTypes
from mongoengine import (
    StringField,
)

__all__ = ['AnalysisCategory']


class AnalysisCategory(AbstractDocument):
    meta = {
        'indexes': [
            'name'
        ]
    }

    name = StringField(required=True)
    category_type = StringField(default=EnumCategoryTypes.other.value)

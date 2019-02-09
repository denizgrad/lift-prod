from abstracts import AbstractDocument
from ..analysis_category.models import AnalysisCategory
from mongoengine import (
    StringField,
    ReferenceField,
    DENY
)

__all__ = ['AnalysisItem']


class AnalysisItem(AbstractDocument):

    _key_analysis_category = ReferenceField(AnalysisCategory, reverse_delete_rule=DENY)

    name = StringField(required=True, unique_with='_key_analysis_category')
    # use_analysis_settings = BooleanField(default=True)

from abstracts import AbstractDocument
from mongoengine import (
    StringField,
    DynamicField,
)

__all__ = ['AnalysisSettings']


class AnalysisSettings(AbstractDocument):

    field_key = StringField(required=True)
    field_value = DynamicField(required=True)

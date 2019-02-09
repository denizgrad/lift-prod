from abstracts import AbstractDocument
from ..quote.models import Quote, Project
from mongoengine import (
    DENY,
    StringField,
    ReferenceField,
    EmbeddedDocumentField,
)

__all__ = ['Analysis']


class Analysis(AbstractDocument):

    _key_project = ReferenceField(Project, reverse_delete_rule=DENY)
    _key_quote = ReferenceField(Quote, reverse_delete_rule=DENY)
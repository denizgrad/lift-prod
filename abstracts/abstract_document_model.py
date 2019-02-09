from datetime import datetime
from helpers.aggregation_helper import get_mongo_lookup, get_mongo_unwind
from modules.organization.models import Organization
from modules.user.models import User
from mongoengine import (
    Document,
    DateTimeField,
    ReferenceField
)

__all__ = ['AbstractDocument']


class AbstractDocument(Document):
    """
        Usage:
            class SomeModel(AbstractDocument):
                ...
    """
    meta = {
        'abstract': True
    }
    _created_date = DateTimeField(default=datetime.utcnow)
    _last_modified_date = DateTimeField()

    _key_created_user = ReferenceField(User)
    _key_last_modified_user = ReferenceField(User)
    _key_owner_user = ReferenceField(User)
    _key_organization = ReferenceField(Organization)

    @staticmethod
    def get_user_lookup(local_field, as_name=None):
        as_name = as_name if as_name else local_field
        return dict(
            lookup=get_mongo_lookup(local_field, 'user', '_id', as_name),
            unwind=get_mongo_unwind(as_name),
            project={
                as_name+'._id': 1,
                as_name+'.first_name': 1,
                as_name+'.last_name': 1,
                as_name+'.full_name': 1,
                as_name+'.roles': 1,
            }
        )

    @staticmethod
    def get_system_default_lookup():
        return dict(
            _key_created_user=AbstractDocument.get_user_lookup('_key_created_user'),
            _key_last_modified_user=AbstractDocument.get_user_lookup('_key_last_modified_user'),
            _key_owner_user=AbstractDocument.get_user_lookup('_key_owner_user'),
            created_company=dict(
                lookup=get_mongo_lookup('_key_organization', 'organization', '_id', '_key_organization'),
                unwind=get_mongo_unwind('_key_organization')
            ),
        )

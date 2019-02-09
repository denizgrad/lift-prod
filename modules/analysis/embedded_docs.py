from ..brand.models import Brand
from mongoengine import (
    IntField,
    FloatField,
    StringField,
    ReferenceField,
    EmbeddedDocument,
)


class MachineEngineSettings(EmbeddedDocument):
    _key_brand = ReferenceField(Brand, required=True)
    motor_gucu = FloatField(required=True)
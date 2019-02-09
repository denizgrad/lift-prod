from enum import Enum
from mongoengine import (
    EmbeddedDocument,
    StringField,
    FloatField,
    IntField
)


__all__ = ['EnumCategoryTypes', 'MachineEngineSettings']


class MachineEngineSettings(EmbeddedDocument):
    tahrik_tipi = StringField(required=True)
    motor_tipi = StringField(required=True)
    motor_hizi = FloatField(required=True, min_value=0, max_value=10)
    motor_gucu = FloatField(required=True, min_value=0, max_value=1000)
    kapasite = IntField(required=True, min_value=0, max_value=100000)


class EnumCategoryTypes(Enum):
    machine_engine = dict(id='machine_engine', embedded_doc=MachineEngineSettings)
    cabin = dict(id='cabin', embedded_doc=EmbeddedDocument)
    door = dict(id='door', embedded_doc=EmbeddedDocument)
    rail = dict(id='rail', embedded_doc=EmbeddedDocument)
    control_panel = dict(id='control_panel', embedded_doc=EmbeddedDocument)
    console = dict(id='console', embedded_doc=EmbeddedDocument)
    employment = dict(id='employment', embedded_doc=EmbeddedDocument)
    regulator = dict(id='regulator', embedded_doc=EmbeddedDocument)
    halat = dict(id='halat', embedded_doc=EmbeddedDocument)
    other = 'other'


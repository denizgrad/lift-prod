from enum import Enum


class EnumFieldTypes(Enum):
    BOOL = '1'
    TEXT = '2'
    FLOAT = '3'
    INT = '4'

    @staticmethod
    def convert_value_as_field_type(value, field_type):
        if field_type == EnumFieldTypes.TEXT.value:
            return str(value)
        elif field_type == EnumFieldTypes.BOOL.value:
            return bool(value)
        elif field_type == EnumFieldTypes.FLOAT.value:
            return float(value)
        elif field_type == EnumFieldTypes.INT.value:
            return int(value)
        else:
            raise TypeError('Bilinmeyen bir alan tipi gönderildi')

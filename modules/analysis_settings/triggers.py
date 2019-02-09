from .enum_types import EnumSettings


class AnalysisSettingsTrigger:

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if hasattr(EnumSettings, document.field_key):
            document.field_value = EnumSettings[document.field_key].value['value_type'](document.field_value)

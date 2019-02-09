from enum import Enum

__all__ = ['EnumSettings']


class EnumSettings(Enum):
    max_kat_sayisi = dict(id='max_kat_sayisi', display='Kat Sayısı (Max)', value_type=int, single_record=True)
    kapasite = dict(id='kapasite', display='Kapasite', suffix='KG', value_type=int)
    motor_gucu = dict(id='motor_gucu', display='Motor Gücü', suffix='KW', value_type=float)
    motor_tipi = dict(id='motor_tipi', display='Motor Tipi', value_type=str)
    motor_hizi = dict(id='motor_hizi', display='Motor Hızı', suffix='M/SN', value_type=float)
    tahrik_tipi = dict(id='tahrik_tipi', display='Motor Tipi', value_type=str)
    yerli_ithal = dict(id='yerli_ithal', display='Tipi', value_type=str)
    #  kapı özellikleri
    kaplama_tipi = dict(id='kaplama_tipi', display='Kaplama Tipi', value_type=str)
    panel_olcusu = dict(id='panel_olcusu', display='Panel Ölçüsü', suffix='mm', value_type=str)
    # kabin özellikleri
    materyal = dict(id='materyal', display='Materyal', value_type=str)



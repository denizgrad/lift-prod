from enum import Enum

__all__ = ('EnumStockType', 'EnumUnitTypes', 'EnumMainUnitTypes')


class EnumStockType(Enum):
    STOCK = '1'  # Hammadde
    SEMI = '2'  # Yarı mamül


class EnumUnitTypes(Enum):
    PIECE = '1'  # Adet
    LENGTH = '2'  # Uzunluk
    WEIGHT = '3'  # Ağırlık
    VOLUME = '4'  # Hacim


class EnumMainUnitTypes(Enum):
    """
    Directly related with EnumUnitTypes like parent - child relation
    In this case parent is the `EnumUnitTypes`
    """
    # EnumUnitTypes.PIECE SUB TYPES
    PIECE = '1-1'
    # EnumUnitTypes.LENGTH SUB TYPES
    km = '2-1'
    hm = '2-2'
    dam = '2-3'
    m = '2-4'
    dm = '2-5'
    cm = '2-6'
    mm = '2-7'
    # EnumUnitTypes.WEIGHT SUB TYPES
    kg = '3-1'
    gr = '3-2'
    cg = '3-3'
    mg = '3-4'
    # EnumUnitTypes.VOLUME SUB TYPES
    lt = '4-1'
    dL = '4-2'
    cL = '4-3'
    mL = '4-4'

from bson import ObjectId
from abstracts.abstract_resource_controller import AbstractResourceController
from helpers.http_helper import HttpHelper
from .models import AnalysisLineItems
from ..brand.models import Brand
from ..stock.models import Stock

__all__ = ['ControllerAnalysisLineItem']


class ControllerAnalysisLineItem(AbstractResourceController):

    def __init__(self):
        self.abstract = super(ControllerAnalysisLineItem, self)
        self.main_model = AnalysisLineItems


class ControllerCreateListFromSettings:

    def __init__(self, analysis_details):
        self.settings = analysis_details
        self.line_items = list()

    def get_line_items(self):
        self.set_rail_rows()
        return HttpHelper.json_from_mongo_json(self.line_items)

    def set_rail_rows(self):
        kabin_ray_olcusu = self.settings['rail']['kabin_ray_olcusu']
        agirlik_ray_olcusu = self.settings['rail']['agirlik_ray_olcusu']
        brand_id = ObjectId(self.settings['rail']['_key_brand'])
        brand = Brand.objects(id=brand_id).first()
        agirlik_filter_dict = dict(
            _key_brand=brand_id,
            analysis_settings__ray_tipi='Ray',
            analysis_settings__ray_olcusu=agirlik_ray_olcusu)
        kabin_filter_dict = dict(
            _key_brand=brand_id,
            analysis_settings__ray_tipi='Ray',
            analysis_settings__ray_olcusu=kabin_ray_olcusu
        )
        agirlik_ray = self.get_stock_by_filter(agirlik_filter_dict)
        kabin_ray = self.get_stock_by_filter(kabin_filter_dict)
        self.set_line_item_dict(
            item_list=agirlik_ray,
            item=agirlik_ray.first(),
            quantity=35,
            name_suffix='(Ağırlık Rayı)',
            brand=brand,
            row_item_type='agirlik_ray',
            row_filters=agirlik_filter_dict
        )
        self.set_line_item_dict(
            item_list=kabin_ray,
            item=kabin_ray.first(),
            quantity=35,
            name_suffix='(Kabin Rayı)',
            brand=brand,
            row_item_type='kabin_ray',
            row_filters=kabin_filter_dict
        )

    def get_stock_by_filter(self, filter_dict):
        return Stock\
            .objects(**filter_dict)\
            .only('id', 'buying_price', 'name', '_key_category', '_key_currency', 'main_unit_type', '_key_brand')\
            .order_by('buying_price')

    def set_line_item_dict(self, item_list, item, quantity=0, name_suffix='', brand=None,
                           row_item_type='', row_filters=None):
        item_dict = dict(
            items=list(),
            name='',
            quantity=quantity,
            brand_name='',
            unit_price=0,
            row_item_type=row_item_type,
            row_filters=row_filters
        )
        if item_list:
            item_dict['items'] = item_list
        if item:
            brand = item._key_brand
            currency = item._key_currency
            item_dict['_key_stock'] = item
            item_dict['unit_price'] = item.buying_price
            item_dict['name'] = '{} {}'.format(item.name, name_suffix)
            item_dict['_key_brand'] = brand.id
            item_dict['brand_name'] = brand.name
            try:
                item_dict['_key_category'] = item._key_category.to_mongo()
            except Exception:
                pass
            try:
                if currency.code == 'USD':
                    item_dict['unit_price'] *= self.settings['analysis_settings']['usd_kuru']
                elif currency.code == 'EUR':
                    item_dict['unit_price'] *= self.settings['analysis_settings']['eur_kuru']
            except Exception:
                pass
        elif brand:
            item_dict['_key_brand'] = brand.id
            item_dict['brand_name'] = brand.name
        self.line_items.append(item_dict)

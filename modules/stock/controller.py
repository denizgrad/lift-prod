from bson import ObjectId
from resources import app
from abstracts.abstract_resource_controller import AbstractResourceController
from ..brand.controller import ControllerBrand
from ..currency.models import Currency
from .models import Stock as MainModel


__all__ = ['ControllerStock']


class ControllerStock(AbstractResourceController):

    def __init__(self):
        self.abstract = super(ControllerStock, self)
        self.main_model = MainModel

    def create(self, create_data):
        self.check_currency_type_or_set(create_data)
        self.check_brand(create_data)
        return self.abstract.create(create_data)

    def update(self, mongoid, update_data):
        self.check_brand(update_data)
        return self.abstract.update(mongoid, update_data)

    def check_currency_type_or_set(self, dict_data):
        if '_key_currency' not in dict_data.keys():
            try:
                dict_data['_key_currency'] = Currency.objects(code='TRY').only('id').first().id
            except Exception as e:
                app.logger.error("*** check_currency_type_or_set occurred an exception: {}".format(e))

    def check_brand(self, data):
        if data['_key_brand'] and isinstance(data['_key_brand'], str):
            if ObjectId.is_valid(data['_key_brand']) is False:
                try:
                    stock_code = data['stock_code']
                    description = '{} stok kodlu ürün için sistem tarafından oluşturuldu'.format(stock_code)
                except KeyError:
                    description = 'Bir stok kalemi ile oluşturuldu'
                brand_data = dict(name=data['_key_brand'], description=description)
                data['_key_brand'] = ControllerBrand().create(brand_data).id

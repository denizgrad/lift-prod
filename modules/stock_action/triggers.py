from ..currency.models import Parity
from .models import StockAction, EnumActionTypes


class StockActionTrigger:

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if not document.id:
            filter_args = dict(_key_organization=document['_key_organization'])
            last_record = StockAction.objects(**filter_args).order_by('-id').first()
            try:
                document.action_no = last_record.action_no + 1
            except AttributeError:
                pass
        cls.prepare_totals_price_from_args(document)
        cls.prepare_parity_from_args(document)

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        print("*** post_save fired: {}".format([kwargs, document.action_type, document.quantity]))
        if document.action_type == EnumActionTypes.GIRIS.value and document.quantity > 0:
            StockActionTrigger.update_stock_unit_price(document._key_stock)
        elif document.action_type == EnumActionTypes.CIKIS.value:
            cls.update_stock_totals(document)

    @classmethod
    def prepare_parity_from_args(cls, document):
        parity_record = Parity.get_parity_by_currency(document['_key_currency'].id)
        if parity_record:
            document._key_parity = parity_record.id
            document.parity_value = parity_record.ask_price

    @classmethod
    def prepare_totals_price_from_args(cls, document):
        if document.unit_price and document.quantity:
            document.total_price = float(document.quantity) * float(document.unit_price)

    @classmethod
    def update_stock_totals(cls, document):
        if document.quantity != 0:
            stock_document = document._key_stock
            stock_document.quantity -= document.quantity
            stock_document.total_price = float(stock_document.quantity) * float(stock_document.unit_price)
            stock_document.save()

    @staticmethod
    def update_stock_unit_price(stock_document):
        _pipeline = list()
        _pipeline.append({'$match': {'_key_stock': stock_document.id}})
        _pipeline.append({'$group': {
            '_id': '$action_type',
            'unit_price': {'$sum': '$unit_price'},
            'quantity': {'$sum': '$quantity'},
            'total_price': {'$sum': '$total_price'}
        }})
        results = StockAction.objects.aggregate(*_pipeline)
        # Reset values
        calculated_unit_price = 0
        total_price_in, quantity_out, quantity_in, current_quantity = 0, 0, 0, 0
        # Recalculate values
        for result in results:
            if result['_id'] == EnumActionTypes.GIRIS.value:
                total_price_in += result['total_price']
                quantity_in += result['quantity']
            else:
                quantity_out += result['quantity']
        current_quantity = float(quantity_in - quantity_out)
        if quantity_in > 0:
            calculated_unit_price = float(total_price_in) / float(quantity_in)
        stock_document.unit_price = calculated_unit_price
        stock_document.quantity = current_quantity
        stock_document.total_price = calculated_unit_price * current_quantity
        stock_document.save()

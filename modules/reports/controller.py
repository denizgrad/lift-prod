import time
import datetime
from bson import ObjectId, json_util
from collections import OrderedDict
from helpers import aggregation_helper
from helpers.http_helper import HttpHelper
from modules.stock.models import Stock


class ControllerReports:
    def __init__(self, response):
        self.response = response

    def get_stock_totals(self, get_args):
        """
        Get all stok grouped by currency type
        :param get_args: dict
        :return: dict
        """
        _pipeline = [
            {
                "$match": {'total_price': {'$gt': 0}}
            },
            {
                "$group": {
                    "_id": "$_key_currency",
                    "total_price": {"$sum": "$total_price"},
                }
            },
            aggregation_helper.get_mongo_lookup('_id', 'currency', '_id', 'included.currency'),
            aggregation_helper.get_mongo_unwind('included.currency')
        ]
        return HttpHelper.json_from_mongo_json(list(Stock.objects.aggregate(*_pipeline)))

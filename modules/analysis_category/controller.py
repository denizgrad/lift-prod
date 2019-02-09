from flask_restful import request
from abstracts.abstract_resource_controller import AbstractResourceController
from helpers.aggregation_helper import get_mongo_lookup, get_mongo_unwind
from .models import AnalysisCategory as MainModel
from .models import EnumCategoryTypes

__all__ = ['ControllerAnalysisCategory']


class ControllerAnalysisCategory(AbstractResourceController):

    def __init__(self):
        self.abstract = super(ControllerAnalysisCategory, self)
        self.main_model = MainModel

    def get(self, get_args):
        if request.args.get('quote_aggregetion', None):
            return self.get_grouped_stock_by_category(get_args)
        return self.abstract.get(get_args)

    def get_grouped_stock_by_category(self, get_args):
        args = self.prepare_paginator_args(get_args)
        args['query'] = self.handle_query_dict(args['query'])
        stock_query = args['query'].pop('stock_query', {})
        _pipeline = list()
        _pipeline.append({'$match': args['query']})
        _pipeline.append(get_mongo_lookup('_id', 'stock', '_key_category', 'stock'))
        _pipeline.append(get_mongo_unwind('stock', False))
        _pipeline.append({'$match': stock_query})
        _pipeline.append({
            '$group': {
                '_id': '$stock._key_brand',
            }
        })
        _pipeline.append(get_mongo_lookup('_id', 'brand', '_id', '_id'))
        _pipeline.append(get_mongo_unwind('_id'))
        result = list(MainModel.objects.aggregate(*_pipeline))
        return result, len(result)

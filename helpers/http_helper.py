import time
from resources import app
from json import loads as json_loads
from bson import json_util
from flask_restful import output_json
from mongoengine import Document, Q

__all__ = ['HttpHelper']


class HttpHelper:

    @staticmethod
    def json_from_mongo_json(data):
        return json_loads(json_util.dumps(data))

    @staticmethod
    def json_response(payload, code):
        headers = {'Content-type': 'application/json'}
        return output_json(payload, code, headers)

    @staticmethod
    def prepare_paginator_args(args):
        """ (dict) -> dict

        Handle paginator args and return query_args

        prepare_paginator_args(dict(query=dumps({'foo': 'bar'})))
        ->
        {
            "query": {"foo": "bar"}
            "order": "-id"
            "page": 1
            "offset": 0
            "limit": 15
            ...
        }
        """
        page = int(args.get('page', 1))
        args['query'] = json_util.loads(args.get('query', '{}'))
        args['limit'] = int(args.get('limit', 15))
        args['page'] = page if page > 0 else 1
        args['offset'] = (args['page'] - 1) * args['limit']
        args['order'] = str(args.get('order', '-id'))
        return args

    @staticmethod
    def run_paginator_query(db_object, get_args):
        """ (Document, dict) -> tuple

        :param {Document} db_object: Model class which will perform query
        :param {dict} get_args: Query params
        :return: (db_cursor, int)
        """
        assert issubclass(db_object, Document), 'db_object must be subclass of `mongoengine.Document`'
        if get_args['text_search']:
            return HttpHelper.perform_text_search(db_object, get_args)
        started = time.time()
        # get cursor count with query
        total_count = db_object.objects(**get_args['query']).count()
        # run query to get results
        result = db_object\
            .objects(**get_args['query'])\
            .order_by(get_args['order'])\
            .skip(get_args['offset'])\
            .limit(get_args['limit'])
        # Log execution performans
        app.logger.warning("*** run_paginator_query execution time: {execution_time}"
                           .format(execution_time=time.time() - started))
        return result, total_count

    @staticmethod
    def perform_text_search(db_object, get_args):
        started = time.time()
        # get cursor count with query
        total_count = db_object.objects(**get_args['query']).search_text(get_args['text_search']).count()
        # run query to get results
        result = db_object \
            .objects(**get_args['query']) \
            .search_text(get_args['text_search'])\
            .order_by('$text_score') \
            .skip(get_args['offset']) \
            .limit(get_args['limit'])
        # Log execution performans
        app.logger.warning("*** perform_text_search execution time: {execution_time}"
                           .format(execution_time=time.time() - started))
        return result, total_count

    @staticmethod
    def clear_invalid_values(dict_to_clear):
        """
        Clear dict before trying to save to mongo
        :param {dict} dict_to_clear: Some create or update dict
        :return: dict
        """
        for key, value in list(dict_to_clear.items()):
            if key.startswith('$'):
                del dict_to_clear[key]
            elif isinstance(value, dict):
                sub_dict_keys = list(value.keys())
                if len(sub_dict_keys) > 0 and sub_dict_keys[0].startswith('$'):
                    del dict_to_clear[key]
        return dict_to_clear

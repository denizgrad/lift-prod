import math
import json
from .http_helper import HttpHelper

__all__ = 'SoftRestResponse'


class SoftRestResponse:

    @staticmethod
    def error(message, detail, code):
        """ (string, string, int) -> dict

        Return standart error response detail

        error('ERROR_MESSAGE', 'Some human readable detail about error')
        ->
        {
            "error": {
                "message": "ERROR_MESSAGE",
                "detail": 'Some human readable detail about error'
            }
        }
        """
        payload = dict(
            message=message,
            detail=detail
        )
        return HttpHelper.json_response(dict(error=payload), code)

    @staticmethod
    def index(list_result, total_count, per_page, current_page, document_name=''):
        """ (list, int, int ,int, str) -> dict

        Return standart index (list fetch) response detail

        index(list_result, 125, 5, 1, 'FooModule')
        ->
        {
            "data": [{}, {}, ...],
            "type": "FooModule"
            "meta": {
                "total_count": 125,
                "total_page": 5,
                "current_page: 1
                "per_page": 25
                "
            }
        }
        """
        if hasattr(list_result, 'to_json'):
            list_result = json.loads(list_result.to_json())
        else:
            list_result = HttpHelper.json_from_mongo_json(list_result)
        meta = dict(
            total_count=total_count,
            total_pages=math.ceil(total_count / per_page),
            current_page=current_page,
            per_page=per_page
        )
        payload = dict(
            data=list_result,
            type=document_name,
            meta=meta
        )
        return HttpHelper.json_response(payload, 200)

    @staticmethod
    def single_item(item_id, item, document_name, created=True):
        """ (str, dict|Document, str) -> dict

        Return standart create response detail

        single_item('DOCUMENT_DB_ID', dict_or_document, 'FooBar')
        ->
        {
            "id": "DOCUMENT_DB_ID",
            "type": "FooBar",
            "attributes": dict
        }
        """
        payload = dict(
            id=item_id,
            type=document_name,
            attributes=HttpHelper.json_from_mongo_json(item),
            created=created
        )
        status_code = 201 if created is True else 200
        return HttpHelper.json_response(payload, status_code)

    @staticmethod
    def delete(item_id, document_name):
        """ (str, str) -> dict

        Return standart delete response detail

        delete('DOCUMENT_DB_ID', 'FooBar')
        ->
        {
            "id": "DOCUMENT_DB_ID",
            "type": "FooBar",
            "deleted": true
        }
        """
        payload = dict(
            id=item_id,
            type=document_name,
            deleted=True
        )
        return HttpHelper.json_response(payload, 200)

    @staticmethod
    def bulk_create(has_error, errors, created_count):
        """ (bool, list, int) -> dict

        :param has_error: Has any errors True or False
        :param errors: Error detail each record and their indexes
        :param created_count: Successfuly created record count
        :return: dict

        bulk_create(True, [{index: 2, 'detail': 'Some Error detail in first record'}, {...}], [2, 6], 4)
        ->
        {
            "hasError": True,
            "errors": [{index: 2, 'detail': 'Some Error detail for second record'}, {...}],
            "createdCount": 4
        }
        """
        payload = dict(
            hasError=has_error,
            errors=errors,
            createdCount=created_count
        )
        print(payload)
        code = 201 if created_count > 0 else 200
        return HttpHelper.json_response(payload, code)

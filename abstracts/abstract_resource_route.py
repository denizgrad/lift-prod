import re

from bson import json_util
from json import dumps
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, NotUniqueError, OperationError
from resources import app
from helpers.http_responses import SoftRestResponse
from modules.route_args import get_args, post_put_args, delete_args
from .abstract_resource_controller import AbstractResourceController


__all__ = ['AbstractResourceRoute']


class AbstractResourceRoute(Resource):
    """
        Usage:
            class SomeRouteClass(AbstractResourceRoute):
                #  Property `controller` must be set and should be an instance of subclass of AbstractResourceController
                self.controller = HERE_YOUR_CONTROLLER
    """
    @property
    def controller(self):
        return self.__controller

    @controller.setter
    def controller(self, value):
        assert issubclass(value, AbstractResourceController), 'value must be subclass of `AbstractResourceController`'
        self.__controller = value()

    def get(self, db_id=None):
        get_params = get_args().parse_args()
        if db_id:
            return self.show(db_id, get_params)
        try:
            result, total_count = self.controller.get(get_args=get_params)
            return SoftRestResponse.index(
                list_result=result,
                total_count=total_count,
                per_page=get_params['limit'],
                current_page=get_params['page'],
                document_name=self.controller.main_model.__name__,
            )
        except Exception as e:
            app.logger.error("*** {} method get occurred an exception: {}"
                             .format(self.controller.main_model.__name__, [e.with_traceback, e, e.args]))
            return SoftRestResponse.error(
                message='SERVER_ERROR',
                detail=e.args,
                code=500
            )

    def show(self, db_id, get_args):
        try:
            result, result_id = self.controller.show(db_id, get_args)
            if result:
                return SoftRestResponse.single_item(
                    item_id=result_id,
                    item=result,
                    document_name=self.controller.main_model.__name__,
                    created=False
                )
            return SoftRestResponse.error(
                message='RECORD_NOT_FOUND',
                detail='Aradağınız kriterlere uygun kayıt bulunamadı',
                code=404
            )
        except Exception as e:
            app.logger.error("*** {} method show occurred an exception: {}"
                             .format(self.controller.main_model.__name__, [e.with_traceback, e, e.args]))
            return SoftRestResponse.error(
                message='SERVER_ERROR',
                detail=e.args,
                code=500
            )

    def put(self, mongoid=None):

        update_data = json_util.loads(dumps(post_put_args().parse_args()))
        if "_id" in update_data["data"]:
            del update_data["data"]["_id"]
        try:
            result = self.controller.update(mongoid, update_data['data'])
            return SoftRestResponse.single_item(
                item_id=str(result.id),
                item=result.to_mongo(),
                document_name=self.controller.main_model.__name__,
                created=False
            )
        except DoesNotExist as e:
            return SoftRestResponse.error(
                message='RECORD_NOT_FOUND',
                detail=e.args,
                code=404
            )
        except NotUniqueError as e:
            return SoftRestResponse.error(
                message='UNIQUE_ERROR',
                detail=e.args,
                code=406
            )
        except Exception as e:
            app.logger.error("*** SERVER_ERROR_PUT data: {}\n*ERROR: {}".format(update_data, e.with_traceback))
            return SoftRestResponse.error(
                message='SERVER_ERROR',
                detail=e.args,
                code=500
            )

    def post(self):
        create_data = json_util.loads(dumps(post_put_args().parse_args()))
        has_bulk_list = create_data['data'].pop('bulk_list', None)
        if has_bulk_list:
            return self.bulk_create(bulk_list=has_bulk_list)
        try:
            result = self.controller.create(create_data['data'])
            return SoftRestResponse.single_item(
                item_id=str(result.id),
                item=result.to_mongo(),
                document_name=self.controller.main_model.__name__,
                created=True
            )
        except NotUniqueError as e:
            return SoftRestResponse.error(
                message='UNIQUE_ERROR',
                detail=e.args,
                code=406
            )
        except Exception as e:
            app.logger.error("*** SERVER_ERROR_POST data: {}\n*ERROR: {}".format(create_data, e.with_traceback))
            return SoftRestResponse.error(
                message='SERVER_ERROR',
                detail=e.args,
                code=500
            )

    def delete(self, db_id=None):
        args_delete = delete_args().parse_args()
        try:
            self.controller.delete(db_id, args_delete)
            return SoftRestResponse.delete(
                item_id=str(db_id),
                document_name=self.controller.main_model.__name__
            )
        except DoesNotExist as e:
            return SoftRestResponse.error(
                message='RECORD_NOT_FOUND',
                detail=e.args,
                code=404
            )
        except OperationError as e:
            matchObj = re.match(".*\({1}([a-z|A-Z]+).{1}.*", e.args[0], flags=0)
            return SoftRestResponse.error(
                message='RECORD_NOT_DELETED',
                detail=matchObj.group(1),
                code=406
            )
        except Exception as e:
            return SoftRestResponse.error(
                message='SERVER_ERROR',
                detail=e.args,
                code=500
            )

    def bulk_create(self, bulk_list):
        result = self.controller.bulk_create(bulk_list)
        return SoftRestResponse.bulk_create(**result)

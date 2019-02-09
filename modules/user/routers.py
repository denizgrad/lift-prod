from mongoengine import DoesNotExist

from abstracts.abstract_resource_route import AbstractResourceRoute
from helpers.http_responses import SoftRestResponse
from modules.permission.constants import EnumPermission
from modules.user.auth.routers import token_required
from modules.user.models import User
from resources import app,api
from modules.user.controller import user_controller
from flask import session, request
from flask_restful import Resource, reqparse
from flask import Response
from modules.route_args_model import getArgs, postArgs, putArgs, deleteArgs
from bson.json_util import dumps,loads

class user_router(AbstractResourceRoute):
    """
    Extends of flask restfull resource
    :param Resource extended class
    """
    def __init__(self):
        self.abstract = super(user_router, self)
        self.controller = user_controller
        self.jobs = user_controller()

    @token_required
    def get(self, mongoid=None):
        app.logger.debug("***{} fired as GET request".format(self.__class__.__name__))
        if mongoid:
            app.logger.debug("get one for id:{}".format(mongoid))
        return self.abstract.get(mongoid)


    def post(self):
        app.logger.debug(("***{} fired as POST request").format(self.__class__.__name__))
        try:
            postRequestArgs = postArgs().parse_args()
            postRequestArgs = postRequestArgs['data']
            # exceptions are handled in controller real response returns
            retUser = self.jobs.create(postRequestArgs)
        except Exception as e:
            app.logger.error(("***{} post method occurred an error").format(self.__class__.__name__))
            app.logger.exception(e.args)
            return Response(None, status=500, mimetype='application/json')

    @token_required
    def put(self, mongoid):
        app.logger.debug(("***{} fired as PUT request").format(self.__class__.__name__))
        putRequestArgs = putArgs().parse_args()
        putRequestArgs = putRequestArgs['data']
        # remove _id javascript field
        putRequestArgs.pop("_id", None)
        app.logger.debug(("***putRequestArgs"+str(putRequestArgs)))
        try:
            retUser = self.jobs.update(mongoid, putRequestArgs)
            return SoftRestResponse.single_item(
                item_id=str(retUser.id),
                item=retUser.to_mongo(),
                document_name='User',
                created=False
            )
        except DoesNotExist as e:
            return SoftRestResponse.error(
                message='RECORD_NOT_FOUND',
                detail=e.args,
                code=404
            )
        except Exception as e:
            return SoftRestResponse.error(
                message='SERVER_ERROR_PUT',
                detail=e.args,
                code=500
            )

    @token_required
    def delete(self, mongoid):
        app.logger.debug("***{} fired as DELETE request with id:{}".format(self.__class__.__name__, mongoid))
        return self.abstract.delete(db_id=mongoid)


# """
#  *** Restful Api register for this module ***
# """

api.add_resource(user_router,
                 '/api/v1/user',
                 '/api/v1/user/<mongoid>',
                 endpoint='api-users',
                 methods=['GET', 'POST', 'PUT', 'DELETE'])

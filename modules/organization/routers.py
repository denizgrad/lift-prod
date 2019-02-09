from abstracts.abstract_resource_route import AbstractResourceRoute
from modules.user.auth.routers import token_required, admin_token_required
from resources import app
from flask_restful import Resource, reqparse
from modules.route_args_model import getArgs, postArgs, putArgs, deleteArgs
from .org_controller import org_controller
from flask import Response, session
from .models import Organization
from bson.json_util import dumps, loads


class RouteOrganization(AbstractResourceRoute):
    """
         Extends of flask restfull resource
         :param Resource extended class
         """

    def __init__(self):
        self.abstract = super(RouteOrganization, self)
        self.controller = org_controller

    @token_required
    def get(self, mongoid=None):
        app.logger.debug("***{} fired as GET request".format(self.__class__.__name__))
        if mongoid:
            app.logger.debug("get one for id:{}".format(mongoid))
        return self.abstract.get(mongoid)

    @token_required
    def post(self):
        app.logger.debug("***{} fired as POST request".format(self.__class__.__name__))
        return self.abstract.post()

    @token_required
    def put(self, mongoid):
        app.logger.debug("***{} fired as PUT request with id:{}".format(self.__class__.__name__, mongoid))
        return self.abstract.put(mongoid=mongoid)

    @admin_token_required
    def delete(self, mongoid):
        app.logger.debug("***{} fired as DELETE request with id:{}".format(self.__class__.__name__, mongoid))
        return self.abstract.delete(db_id=mongoid)


app.logger.debug("*** RouteOrganization api")
app.api.add_resource(RouteOrganization,
                 '/api/v1/organization',
                 '/api/v1/organization/<mongoid>',
                     endpoint='api-Organization',
                     methods=['GET', 'POST', 'PUT', 'DELETE'])
from flask import Response, session

from abstracts.abstract_resource_route import AbstractResourceRoute
from modules.analyzes.cabin.cabintypes.models import CabinType
from modules.analyzes.cabin.models import Cabin
from modules.organization.models import Organization
from modules.user.models import User
from resources import app
from flask_restful import Resource, reqparse
from modules.user.auth.routers import token_required
from .controller import ControllerCabinTypes
from modules.route_args_model import postArgs
from bson.json_util import dumps

class router_cabinType(AbstractResourceRoute):
    """
        Extends of flask restfull resource
        :param Resource extended class
        """

    def __init__(self):
        self.abstract = super(router_cabinType, self)
        self.controller = ControllerCabinTypes

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

    @token_required
    def delete(self, mongoid):
        app.logger.debug("***{} fired as DELETE request with id:{}".format(self.__class__.__name__, mongoid))
        return self.abstract.delete(db_id=mongoid)


app.logger.debug("*** Route Cabin Types api")
app.api.add_resource(router_cabinType,
                     '/api/v1/cabin/type',
                     '/api/v1/cabin/type/<mongoid>',
                     endpoint='api-cabin-type',
                     methods=['GET', 'POST', 'PUT', 'DELETE'])

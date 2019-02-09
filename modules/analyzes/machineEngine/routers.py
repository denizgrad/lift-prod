from bson.json_util import dumps, loads
from flask import Response, session
from flask_restful import Resource, reqparse

from abstracts.abstract_resource_route import AbstractResourceRoute
from modules.analyzes.machineEngine.capacity.models import Capacity
from modules.analyzes.machineEngine.controller import ControllerMachineEngine
from modules.analyzes.machineEngine.enginespeed.models import EngineSpeed
from modules.analyzes.machineEngine.enginetype.models import EngineType
from modules.analyzes.machineEngine.models import MachineEngine
from modules.analyzes.machineEngine.roomtype.models import EngineRoomType
from modules.analyzes.machineEngine.volume.models import Volume
from modules.currency.models import Currency
from modules.discount.models import Discount
from modules.helper2 import helper
from modules.organization.models import Organization
from modules.route_args_model import postArgs
from modules.user.auth.routers import token_required
from resources import app


class router_machineEngine(AbstractResourceRoute):
    """
         Extends of flask restfull resource
         :param Resource extended class
         """

    def __init__(self):
        self.abstract = super(router_machineEngine, self)
        self.controller = ControllerMachineEngine

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


app.logger.debug("*** Route Machine Engine api")
app.api.add_resource(router_machineEngine,
                     '/api/v1/engine',
                     '/api/v1/engine/<mongoid>',
                     endpoint='api-engine',
                     methods=['GET', 'POST', 'PUT', 'DELETE'])

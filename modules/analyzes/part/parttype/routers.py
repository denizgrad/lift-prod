from abstracts.abstract_resource_route import AbstractResourceRoute
from modules.user.auth.routers import token_required
from resources import app
from .controller import Controller


class router_partType(AbstractResourceRoute):
    """
         Extends of flask restfull resource
         :param Resource extended class
         """

    def __init__(self):
        self.abstract = super(router_partType, self)
        self.controller = Controller

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


app.logger.debug("*** Route Analyze Part Api")
app.api.add_resource(
    router_partType,
    '/api/v1/part/type',
    '/api/v1/part/type/<mongoid>',
    endpoint='api-part-type',
    methods=['GET', 'POST', 'PUT', 'DELETE']
)

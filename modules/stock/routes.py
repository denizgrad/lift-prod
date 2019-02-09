from abstracts.abstract_resource_route import AbstractResourceRoute
from modules.user.auth.routers import token_required
from .controller import ControllerStock as MainController


class route_stock(AbstractResourceRoute):

    def __init__(self):
        self.abstract = super(route_stock, self)
        self.controller = MainController

    @token_required
    def get(self, db_id=None):
        return self.abstract.get(db_id)

    @token_required
    def post(self):
        return self.abstract.post()

    @token_required
    def put(self, db_id=None):
        return self.abstract.put(db_id)

    @token_required
    def delete(self, db_id=None):
        return self.abstract.delete(db_id)

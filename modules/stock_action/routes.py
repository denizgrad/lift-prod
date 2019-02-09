from abstracts.abstract_resource_route import AbstractResourceRoute
from modules.user.auth.routers import token_required
from ..route_args import post_put_args
from .controller import ControllerStockAction as MainController


class route_stockaction(AbstractResourceRoute):

    def __init__(self):
        self.abstract = super(route_stockaction, self)
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

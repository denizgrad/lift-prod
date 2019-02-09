from abstracts.abstract_resource_route import AbstractResourceRoute
from modules.user.auth.routers import token_required
from .controller import Controller as MainController


class route_parity(AbstractResourceRoute):

    def __init__(self):
        self.abstract = super(route_parity, self)
        self.controller = MainController

    @token_required
    def get(self, db_id=None):
        return self.abstract.get(db_id)

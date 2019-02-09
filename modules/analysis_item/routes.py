from abstracts.abstract_resource_route import AbstractResourceRoute
from modules.user.auth.routers import token_required
from .controller import ControllerAnalysisItem as MainController

__all__ = ['route_analysisitem']


class route_analysisitem(AbstractResourceRoute):

    def __init__(self):
        self.abstract = super(route_analysisitem, self)
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

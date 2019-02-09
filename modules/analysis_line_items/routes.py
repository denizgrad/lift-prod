from flask_restful import Resource
from modules.route_args import post_put_args
from abstracts.abstract_resource_route import AbstractResourceRoute
from modules.user.auth.routers import token_required
from .controller import ControllerCreateListFromSettings, ControllerAnalysisLineItem as MainController


__all__ = ['route_analysislineitems', 'route_recalculatelineitems']


class route_analysislineitems(AbstractResourceRoute):

    def __init__(self):
        self.abstract = super(route_analysislineitems, self)
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


class route_recalculatelineitems(Resource):

    @token_required
    def post(self):
        post_args = post_put_args().parse_args()
        return ControllerCreateListFromSettings(post_args['data']).get_line_items(), 201

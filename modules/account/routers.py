from abstracts.abstract_resource_route import AbstractResourceRoute
from modules.account.controller import Controller
from modules.user.auth.routers import token_required


class route_account(AbstractResourceRoute):
    """
         Extends of flask restfull resource
         :param Resource extended class
         """

    def __init__(self):
        self.abstract = super(route_account, self)
        self.controller = Controller

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

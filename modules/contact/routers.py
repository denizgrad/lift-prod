from abstracts.abstract_resource_route import AbstractResourceRoute
from modules.contact.controller import Controller as MainController
from modules.user.auth.routers import token_required


class route_contact(AbstractResourceRoute):
    """
         Extends of flask restfull resource
         :param Resource extended class
         """

    def __init__(self):
        self.abstract = super(route_contact, self)
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

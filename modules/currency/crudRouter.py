from flask import app

from abstracts import AbstractResourceRoute
from modules.currency.crudController import CrudController
from modules.user.auth.routers import token_required


class route_currency(AbstractResourceRoute):

    def __init__(self):
        self.abstract = super(route_currency, self)
        self.controller = CrudController

    @token_required
    def get(self, db_id=None):
        return self.abstract.get(db_id)

    @token_required
    def post(self):
        return self.abstract.post()

    @token_required
    def put(self, db_id=None):
        return self.abstract.put(db_id)


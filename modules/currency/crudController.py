
from abstracts.abstract_resource_controller import AbstractResourceController
from modules.currency.models import Currency


class CrudController(AbstractResourceController):
    def __init__(self):
        self.abstract = CrudController
        self.main_model = Currency
        self.default_kwargs = dict()

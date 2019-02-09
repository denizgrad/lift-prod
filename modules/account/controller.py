from abstracts.abstract_resource_controller import AbstractResourceController

from modules.account.models import Accounts as MainModel


class Controller(AbstractResourceController):
    def __init__(self):
        self.abstract = super(Controller, self)
        self.main_model = MainModel

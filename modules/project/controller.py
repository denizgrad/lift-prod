from abstracts.abstract_resource_controller import AbstractResourceController
from modules.project.models import Project as MainModel


class Controller(AbstractResourceController):
    def __init__(self):
        self.abstract = super(Controller, self)
        self.main_model = MainModel

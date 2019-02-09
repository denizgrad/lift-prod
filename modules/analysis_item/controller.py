from abstracts.abstract_resource_controller import AbstractResourceController
from .models import AnalysisItem as MainModel

__all__ = ['ControllerAnalysisItem']


class ControllerAnalysisItem(AbstractResourceController):

    def __init__(self):
        self.abstract = super(ControllerAnalysisItem, self)
        self.main_model = MainModel

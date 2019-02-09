from abstracts.abstract_resource_controller import AbstractResourceController
from .models import AnalysisSettings as MainModel

__all__ = ['ControllerAnalysisSettings']


class ControllerAnalysisSettings(AbstractResourceController):

    def __init__(self):
        self.abstract = super(ControllerAnalysisSettings, self)
        self.main_model = MainModel

from abstracts.abstract_resource_controller import AbstractResourceController
from .models import Analysis

__all__ = ['ControllerAnalysis']


class ControllerAnalysis(AbstractResourceController):

    def __init__(self):
        self.abstract = super(ControllerAnalysis, self)
        self.main_model = Analysis

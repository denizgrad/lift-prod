from abstracts.abstract_resource_controller import AbstractResourceController
from .models import Brand


class ControllerBrand(AbstractResourceController):
    def __init__(self):
        self.abstract = super(ControllerBrand, self)
        self.main_model = Brand

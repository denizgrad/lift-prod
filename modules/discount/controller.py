from abstracts.abstract_resource_controller import AbstractResourceController
from modules.helper2 import helper
from .models import Discount


class ControllerDiscount(AbstractResourceController):
    def __init__(self):
        self.helper = helper()
        self.abstract = super(ControllerDiscount, self)
        self.main_model = Discount
        self.default_kwargs = dict()

    def get(self, get_args):
        return self.abstract.get(get_args)

    def create(self, data):
        return self.abstract.create(data)

    def update(self, mongoid, data):
        return self.abstract.update(mongoid, data)

    def delete(self, mongoid):
        return self.abstract.delete(mongoid)
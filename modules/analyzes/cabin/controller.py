import datetime

from flask import session

from abstracts.abstract_resource_controller import AbstractResourceController
from modules.helper2 import helper

from .models import Cabin

__all__ = ["ControllerCabin"]

class ControllerCabin(AbstractResourceController):
    def __init__(self):
        self.helper = helper()
        self.abstract = super(ControllerCabin, self)
        self.main_model = Cabin
        self.default_kwargs = dict()

    def get(self, get_args):
        return self.abstract.get(get_args)

    def create(self, data):
        return self.abstract.create(data)

    def update(self, mongoid, data):
        return self.abstract.update(mongoid, data)

    def delete(self, mongoid):
        return self.abstract.delete(mongoid)




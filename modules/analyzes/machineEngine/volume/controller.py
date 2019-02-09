from abstracts.abstract_resource_controller import AbstractResourceController
from modules.analyzes.machineEngine.volume.models import Volume
from modules.helper2 import helper


class ControllerVolume(AbstractResourceController):
    def __init__(self):
        self.helper = helper()
        self.abstract = super(ControllerVolume, self)
        self.main_model = Volume
        self.default_kwargs = dict()

    def get(self, get_args):
        return self.abstract.get(get_args)

    def create(self, data):
        return self.abstract.create(data)

    def update(self, mongoid, data):
        return self.abstract.update(mongoid, data)

    def delete(self, mongoid):
        return self.abstract.delete(mongoid)
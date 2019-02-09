from modules.analyzes.controlPanel.panelsize.models import ControlPanelSize
from modules.helper2 import helper as helper


class Controller:
    def __init__(self):
        self.helper = helper()
        self.abstract = super(Controller, self)
        self.main_model = ControlPanelSize
        self.default_kwargs = dict()

    def get(self, get_args):
        return self.abstract.get(get_args)

    def create(self, data):
        return self.abstract.create(data)

    def update(self, mongoid, data):
        return self.abstract.update(mongoid, data)

    def delete(self, mongoid):
        return self.abstract.delete(mongoid)
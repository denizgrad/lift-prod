import datetime
from resources import app
from pprint import pprint
from flask import Response, session
from bson.json_util import dumps

from modules.analyzes.controlPanel.controlpanelextra.models import ControlPanelExtra
from modules.user.models import User
from modules.organization.models import Organization
from modules.liftnec_utils import remove_none_key
from modules.helper2 import helper as helper


class Controller:
    def __init__(self):
        self.helper = helper()
        self.abstract = super(Controller, self)
        self.main_model = ControlPanelExtra
        self.default_kwargs = dict()

    def get(self, get_args):
        return self.abstract.get(get_args)

    def create(self, data):
        return self.abstract.create(data)

    def update(self, mongoid, data):
        return self.abstract.update(mongoid, data)

    def delete(self, mongoid):
        return self.abstract.delete(mongoid)
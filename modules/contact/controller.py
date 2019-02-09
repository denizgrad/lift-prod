from abstracts.abstract_resource_controller import AbstractResourceController
from modules.contact.models import Contact


class Controller(AbstractResourceController):
    def __init__(self):
        self.abstract = super(Controller, self)
        self.main_model = Contact

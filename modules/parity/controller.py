from abstracts.abstract_resource_controller import AbstractResourceController
from .models import Parity as MainModel


class Controller(AbstractResourceController):
    def __init__(self):
        self.abstract = super(Controller, self)
        self.main_model = MainModel
        self.default_kwargs = dict()
        self.default_create_data = dict()

    def update(self, document_id, delete_args):
        raise PermissionError("Parite güncelleme yetkisine sahip değilsiniz")

    def delete(self, document_id, delete_args):
        raise PermissionError("Parite silme yetkisine sahip değilsiniz")
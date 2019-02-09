from abstracts.abstract_resource_controller import AbstractResourceController
from modules.permission.constants import EnumPermission

from .models import Permission
from ..helper2 import helper as helper


class Controller(AbstractResourceController):
    def __init__(self):
        self.helper = helper()
        self.abstract = super(Controller, self)
        self.main_model = Permission
        self.default_kwargs = dict()

    def get(self, get_args):
        return self.abstract.get(get_args)

    def create(self, data):
        return self.abstract.create(data)

    def update(self, mongoid, data):
        return self.abstract.update(mongoid, data)

    def delete(self, mongoid):
        return self.abstract.delete(mongoid)

    def create_default(self, org_obj = None):
        for module_name in self.helper.listModules():
            for role_name in self.helper.listRoles():
                    if role_name == EnumPermission.FIRMA_ADMIN.value or role_name == EnumPermission.SIRKET_YONETICI.value:
                        permission = Permission(organization=org_obj,
                                                module_name=module_name,
                                                role_name=role_name,
                                                action_list= self.helper.listActions())
                        permission.save()
                    else:
                        permission = Permission(organization = org_obj,
                                                module_name=module_name,
                                                role_name = role_name,
                                                action_list=["get"])
                        permission.save()
        return None
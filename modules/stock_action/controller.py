from flask import session
from abstracts.abstract_resource_controller import AbstractResourceController
from .models import StockAction as MainModel, Parity, EnumActionTypes

__all__ = ['ControllerStockAction']


class ControllerStockAction(AbstractResourceController):
    """
        StockAction model uses Safe Delete login for deletion
        Tell this to abstract model with `is_safe_delete_avaible=True`
    """

    def __init__(self):
        self.abstract = super(ControllerStockAction, self)
        self.main_model = MainModel
        self.is_safe_delete_avaible = True




    def update_stock_prices(self, stock_id, record_stock_action):
        pass
from resources import app
from flask import session
from modules.user.models import User
from modules.stock_action.models import StockAction


class StockTrigger:

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        pass

    @classmethod
    def pre_delete(cls, sender, document, **kwargs):
        if 'forceDelete' in kwargs and kwargs['forceDelete']:
            current_user = User.objects(id=session['current_user_id']).first()
            app.logger.warning("*** {}.pre_delete fired with attribute `forceDelete` by: {}"
                               .format(cls.__name__, current_user.full_name))
            try:
                for action in StockAction.objects(_key_stock=document.id):
                    action.delete()
            except Exception as e:
                app.logger.error("*** {}.pre_delete.force_delete occurred an exception *ERROR: {}"
                                 .format(cls.__name__, [e, e.with_traceback]))

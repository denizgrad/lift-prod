from mongoengine import signals
from modules.contact import Contact, ContactTrigger
from modules.user.models import User
from modules.user.triggers import UserTrigger
from modules.stock.models import Stock
from modules.stock.triggers import StockTrigger
from modules.stock_action.models import StockAction
from modules.stock_action.triggers import StockActionTrigger
from modules.analysis_item.models import AnalysisItem
from modules.analysis_item.triggers import AnalysisItemTrigger
from modules.analysis_settings.models import AnalysisSettings
from modules.analysis_settings.triggers import AnalysisSettingsTrigger

# ======== Register Signals START ========
# pre_save signals
signals.pre_save.connect(UserTrigger.pre_save, sender=User)
signals.pre_save.connect(ContactTrigger.pre_save, sender=Contact)
signals.pre_save.connect(StockTrigger.pre_save, sender=Stock)
signals.pre_save.connect(StockActionTrigger.pre_save, sender=StockAction)
signals.pre_save.connect(AnalysisItemTrigger.pre_save, sender=AnalysisItem)
signals.pre_save.connect(AnalysisSettingsTrigger.pre_save, sender=AnalysisSettings)
# post_save signals
signals.post_save.connect(StockActionTrigger.post_save, sender=StockAction)
#
signals.pre_delete.connect(StockTrigger.pre_delete, sender=Stock)


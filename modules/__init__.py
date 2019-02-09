"""
    Register app rest routes and blueprints with modules
"""
# Daily schedule
from . import daily_schedule
from .currency.controller import Controller as CurrencyCtrl

# Add update_rates to daily schedule list
daily_schedule.register_methods_to_daily_job(func='update_rates', cls=CurrencyCtrl)

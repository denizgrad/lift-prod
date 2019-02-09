from modules.currency.crudRouter import route_currency
from resources import api
from .analysis_item.routes import route_analysisitem
from .analysis_category.routes import route_analysiscategory
from .analysis_settings.routes import route_analysissettings
from .stock.routes import route_stock
from .stock_action.routes import route_stockaction
from .account.routers import route_account
from .contact.routers import route_contact
from .quote.routers import route_quote
from .project import route_project
from .reports import route_reports
from .parity import route_parity
from .analysis_line_items import route_recalculatelineitems

# Parity Route
api.add_resource(route_parity,
                 '/api/v1/parity',
                 methods=['GET'])
# Reports Route
api.add_resource(route_reports,
                 '/api/v1/reports/<action_name>',
                 methods=['GET'])
# Analysis Module
api.add_resource(route_analysisitem,
                 '/api/v1/analysis-item',
                 '/api/v1/analysis-item/<db_id>',
                 endpoint='api_analysis-item', methods=['GET', 'POST', 'PUT', 'DELETE'])
api.add_resource(route_analysiscategory,
                 '/api/v1/analysis-category',
                 '/api/v1/analysis-category/<db_id>',
                 endpoint='api_analysis-category', methods=['GET', 'POST', 'PUT', 'DELETE'])
api.add_resource(route_analysissettings,
                 '/api/v1/analysis-settings',
                 '/api/v1/analysis-settings/<db_id>',
                 endpoint='api_analysis-category-settings', methods=['GET', 'POST', 'PUT', 'DELETE'])
# Stock (Stok-Depo) Module
api.add_resource(route_stock,
                 '/api/v1/stock',
                 '/api/v1/stock/<db_id>',
                 endpoint='api_stock', methods=['GET', 'POST', 'PUT', 'DELETE'])
api.add_resource(route_stockaction,
                 '/api/v1/stock-action',
                 '/api/v1/stock-action/<db_id>',
                 endpoint='api_stock_action', methods=['GET', 'POST', 'PUT', 'DELETE'])
# Account Module
api.add_resource(route_account,
                 '/api/v1/account',
                 '/api/v1/account/<db_id>',
                 endpoint='api_account', methods=['GET', 'POST', 'PUT', 'DELETE'])
# Contact Module
api.add_resource(route_contact,
                 '/api/v1/contact',
                 '/api/v1/contact/<db_id>',
                 endpoint='api_contact', methods=['GET', 'POST', 'PUT', 'DELETE'])
# Project Module
api.add_resource(route_project,
                 '/api/v1/project',
                 '/api/v1/project/<db_id>',
                 endpoint='api_project', methods=['GET', 'POST', 'PUT', 'DELETE'])
# Quote Module
api.add_resource(route_quote,
                 '/api/v1/quote',
                 '/api/v1/quote/<db_id>',
                 endpoint='api_quote', methods=['GET', 'POST', 'PUT', 'DELETE'])
# Currency Module
api.add_resource(route_currency,
                 '/api/v1/currency',
                 '/api/v1/currency/<id>',
                 endpoint='api-currency', methods=['GET', 'POST', 'PUT', 'DELETE'])

# Quote Analysis Line Items Recalculator
api.add_resource(
    route_recalculatelineitems,
    '/api/v1/quote-analysis-recalculate',
    endpoint='api_quote_recalculatelineitems',
    methods=['POST']
)
from resources import app
from flask_restful import Resource
from modules.user.auth.routers import token_required
from .controller import ControllerAdminJobs


class RouteAdminJobs(Resource):
    """
    Extends of flask restful resource for RouteAdminJobs
    :param Resource extended class
    """

    def __init__(self):
        self.jobs = ControllerAdminJobs()

    @token_required
    def get(self, secret_key=None, action_name=None):
        if secret_key != 'a1795592-ee15-40ab-b310-e675f4656f85':
            return "Geçersiz Anahtar", 406
        if action_name is None:
            return "Çalıştırılacak Method Belirtilmedi", 406
        if action_name not in dir(self.jobs):
            return "Belirtilen Method Tanımlı Değil", 406
        else:
            return self.jobs.__getattribute__(action_name)()


app.api.add_resource(
    RouteAdminJobs,
    '/api/admin/runable-jobs',
    '/api/admin/runable-jobs/<secret_key>',
    '/api/admin/runable-jobs/<secret_key>/<action_name>',
    endpoint='api-admin-runable-jobs',
    methods=['GET']
)
import time
import json
from bson import json_util
from flask_restful import Resource
from modules.user.auth.routers import token_required
from modules.route_args import get_args
from .controller import ControllerReports


class route_reports(Resource):
    """
    Extends of flask restfull resource
    :param Resource extended class
    """
    def __init__(self):
        self.response = {
            "hasError": False,
            "detail": '',
            "data": None
        }
        self.controller = ControllerReports(self.response)

    @token_required
    def get(self, action_name):
        get_request_args = json_util.loads(json.dumps(get_args().parse_args()))
        if action_name is None:
            self.response["hasError"] = True
            self.response["errorCode"] = "NO_action_name_SPECIFIED"
            self.response["detail"] = "{}.get method requires action_name paramater".format(self.__class__.__name__)
            return self.response, 406
        else:
            if action_name not in dir(self.controller):
                self.response["hasError"] = True
                self.response["detail"] = "Unknown action_name requested"
                return self.response, 406
            action_name_method = self.controller.__getattribute__(action_name)
            if callable(action_name_method):
                proccess_started_time = time.time()
                self.response["data"] = action_name_method(get_request_args)
                self.response["proccess_execution_time"] = time.time() - proccess_started_time
                return self.response, 200
            else:
                self.response["hasError"] = True
                self.response["detail"] = "action_name does not callable"
                return self.response, 406

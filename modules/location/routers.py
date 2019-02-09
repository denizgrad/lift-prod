import mongoengine
from bson.json_util import dumps, loads
from flask_login import login_required
from flask_restful import Resource

from get_all_request_parser import GetAllRequestParser
from modules.route_args_model import getArgs, postArgs
from modules.location.controller import LocationController
from modules.location.models import Location
from resources import app


class LocationRoute(Resource):
    def __init__(self):
        self.jobs = LocationController()

    @login_required
    def get(self, mongoid=None):
        get_args = getArgs()
        get_args.add_argument("loadPreSurvey", default=1, type=int,
                              help="Ön ekspertiz verileri yüklensin mi? 0 ve 1 değerlerini alır")
        get_args.add_argument("loadPreSurveyDetails", default=1, type=int,
                              help="Ön ekspertiz işçilik ve yedek parça verileri yüklensin mi? 0 ve 1 değerlerini alır")
        getRequestArgs = get_args.parse_args()
        if mongoid:
            return Location.objects(id=mongoid).first().to_json(), 200
        else:
            request_parser = GetAllRequestParser(Location, getRequestArgs, None, None)
            # parse arguments and return result
            result = request_parser.run()
            return result

    @login_required
    def post(self):
        """
        :param data:  POST argument for damage record values
        :return: JSON acceptance record
        """
        app.logger.debug("***{} fired as POST request".format(self.__class__.__name__))
        try:
            post_request_args = postArgs().parse_args()
            app.logger.debug("****(post_request_args['data']" + str(post_request_args['data']))
            damage = self.jobs.create(post_request_args['data'])
            app.logger.debug("*** damage " + str(damage.to_mongo()))
            return dumps(loads(damage.to_json())), 201
        except Exception as e:
            app.logger.error(("***{} post method occurred an error").format(self.__class__.__name__))
            app.logger.exception(e.args)
            return e.args, 500

    @login_required
    def delete(self,mongoid):
        try:
            return self.jobs.delete(mongoid) , 201
        except Exception as e:
            app.logger.error(("***{} post method occurred an error").format(self.__class__.__name__))
            app.logger.exception(e.args)
            return e.args, 500

app.api.add_resource(LocationRoute,
                 '/api/v1/location/',
                 '/api/v1/location/<mongoid>',
                 endpoint='api-location',
                 methods=['GET', 'POST', 'PUT', 'DELETE'])
from get_all_request_parser import GetAllRequestParser
from resources import app,api
from flask_restful import Resource
from flask_login import login_required, current_user
from modules.route_args_model import getArgs, postArgs, putArgs, deleteArgs
from .models import Message
from .controller import Controller
from bson.json_util import dumps,loads
from bson.objectid import ObjectId



class RouteMessage(Resource):
    """
        Extends of flask restfull resource
        :param Resource extended class
        """

    def __init__(self):
        self.jobs=Controller()

    @login_required
    def get(self,mongoid=None):
        get_args = getArgs()
        get_args.add_argument('advanced_message_query', type=str,
                              help='Şirketin sadece ilişkili dosyalara erişim sağlama kontrollerini hazırlar')
        getRequestArgs = get_args.parse_args()
        if mongoid:
            return Message.objects(id=mongoid).first().to_json(),201
        else:
            request_parser = GetAllRequestParser(Message,getRequestArgs,None,None)
            # parse arguments and return result
            return request_parser.run()

    @login_required
    def post(self):
        app.logger.debug(("***{} fired as POST request").format(self.__class__.__name__))
        try:
            post_request_args = postArgs().parse_args()
            app.logger.debug("****(post_request_args['data']"+str(post_request_args['data']))
            message = self.jobs.create(post_request_args['data'])
            app.logger.debug("*** damage "+str(message.to_mongo()))
            return dumps(loads(message.to_json())), 201
        except Exception as e:
            app.logger.error(("***{} post method occurred an error").format(self.__class__.__name__))
            app.logger.exception(e.args)
            return e.args, 500




app.logger.debug("*** RouteCompany api")
api.add_resource(RouteMessage,
                 '/api/v1/message/',
                 '/api/v1/message/<mongoid>',
                 endpoint='message',
                 methods=['GET', 'POST', 'PUT', 'DELETE'])
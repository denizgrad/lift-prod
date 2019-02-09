import copy
import re

from get_all_request_parser import GetAllRequestParser
from resources import app
from flask_restful import Resource, Api, reqparse

from flask_login import login_required, current_user
from bson.json_util import dumps
from modules.route_args_model import postArgs, getArgs
from json import loads
from .models import Notification
from ..helper2 import helper
from mongoengine.queryset.visitor import Q
from .controller import Controller
from resources import api


class RouteNotification(Resource):


    @login_required
    def get(self, mongoId: object = None) -> object:
        app.logger.debug("***message fired as GET request")
        if mongoId is None:
            getMessageArgs = getArgs().parse_args()
            if getMessageArgs.get('nin', None) is not None and getMessageArgs.get('ninfname', None) is None:
                app.logger.debug("***getMessages nin param : "+str(getMessageArgs['nin']))
                ninArray=getMessageArgs['nin'].split(",")
                tempArray=[]
                for arrayel in ninArray:
                    if  arrayel != "":
                        tempArray.append(int(arrayel))
                if len(ninArray) > 0:
                    app.logger.debug("***nin"+str(ninArray))
                    result=Notification.objects((Q(reads_by__not = re.compile(current_user.id)) & Q(message_no__nin = tempArray)) ).only("message","message_no")[:10].order_by("-created_date")
                    #result = mongo.db.message.find( {"$and":[{"reads_by":{"$not": re.compile(current_user.id)}},{"message_no":{"$nin":tempArray}}]},
                                                   #{"message": 1, "message_no": 1}).limit(10).sort([("created_at",-1)])
                else :
                    app.logger.debug("***not nin")
                    result = Notification.objects(reads_by__not=re.compile(current_user.id)).only("message", "id")[
                             :10].order_by("-created_date")

                resultDumps=dumps(result)
                app.logger.debug("***resultDump: "+resultDumps)
                return resultDumps
            else:
                request_parser = GetAllRequestParser(Notification, getMessageArgs, None, None)
                # parse arguments and return result
                return request_parser.run()
        else:
            return Notification.objects(id=helper.stringIdToObjectId(mongoId)).first()

    @login_required
    def post(self):
        try:
            postMessageArgs = postArgs().parse_args()
            postMessageArgs = postMessageArgs['data']
            notification=Controller.create(postMessageArgs)
            return notification,201
        except Exception as e:
            app.logger.error("***message post method parse_args occurred an error")
            app.logger.exception(e.args)
            return e.args,500

    @login_required
    def put(self):
        app.logger.debug("***message fired as PUT request")
        try:
            messageArgs = reqparse.RequestParser()
            messageArgs.add_argument('in')
            getMessageArgs = messageArgs.parse_args()
            if getMessageArgs.get('in', None) is not None:
                inArray=getMessageArgs['in'].split(",")
                if len(inArray) > 0:
                    # inArray = list(map(lambda x: int(x), inArray))
                    app.logger.debug("***message_no list to update : "+str(inArray))
                    result=Notification.objects(message_no__in=inArray).update(push__reads_by=str(current_user.userid))
                    #result = mongo.db.message.update_many({"message_no": {"$in": inArray}},{"$push": { "reads_by": current_user.id }})
                    app.logger.debug("***message update result : "+str(result))
                    return True, 201
                else:
                    return "Parametre boş gönderilemez", 406
            else:
                return "Okunacak bildirim belirtilmedi", 406
        except Exception as e:
            app.logger.error("***message PUT method occurred an error")
            app.logger.exception(e.args)
            return e.args,500


class RouteNotificationBulk(Resource):
    @login_required
    def get(self) -> object:
        app.logger.debug("***messageBULK fired as get request")
        return None
    @login_required
    def post(self):
        app.logger.debug("***messageBULK fired as post request")
        try:

            #result = mongo.db.message.update_many({"reads_by": {"$ne": current_user.id}},
             #                                     {"$push": {"reads_by":current_user.id }})
            result = Notification.objects(reads_by__nin=str(current_user.userid)).update(push__reads_by=str(current_user.userid))
            app.logger.debug("***message update result : " + str(result))
            return True, 201
        except Exception as e:
            app.logger.error("***message PUT method occurred an error")
            app.logger.exception(e.args)
            return e.args, 500


api.add_resource(RouteNotification,
                 '/api/v1/notification/',
                 '/api/v1/notification/<mongoId>',
                 endpoint='module/message/',
                 methods=['GET', 'POST', 'PUT'])
api.add_resource(RouteNotificationBulk,'/api/v1/notification-bulk/')

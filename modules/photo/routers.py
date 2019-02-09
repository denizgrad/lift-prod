import os
import uuid

import werkzeug
from bson import ObjectId, DBRef
from werkzeug.utils import secure_filename

from get_all_request_parser import GetAllRequestParser
from modules.photo.controller import Controller
from resources import app,api
from flask_restful import Resource
from flask_login import login_required
from modules.route_args_model import getArgs, postArgs, putArgs, deleteArgs
from flask_restful import reqparse
from .models import Photo
from json import dumps,loads
from modules.message.controller import Controller as MessageCont


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    app.logger.debug("*** filename: "+filename)
    if filename.split(".")[1].lower() in ALLOWED_EXTENSIONS:
        return True
    else:
        return False




class RoutePhoto(Resource):
    """
        Extends of flask restfull resource
        :param Resource extended class
        """

    def __init__(self):
         self.jobs=Controller()


    @login_required
    def post(self):
        """
        body params:
        file: Uploaded file
        title: Title of the file
        description : Description of the file
        related_to : Related record mongo id
        :return: JSON Photo object
        """
        app.logger.debug(("***{} fired as POST request").format(self.__class__.__name__))
        try:
            # create argument parser for file
            file_parser = reqparse.RequestParser()
            # HTTP multipart form file should be accessed with given params
            file_parser.add_argument('file',type=werkzeug.datastructures.FileStorage, location='files')
            file_parser.add_argument('title')
            file_parser.add_argument('description')
            file_parser.add_argument('related_to_user')
            file_parser.add_argument('related_to_message')
            file_parser.add_argument('related_to_company')
            file_parser.add_argument('related_to_field')

            post_request_args = file_parser.parse_args()
            # set file object
            file = post_request_args['file']
            if file and allowed_file(file.filename):
                file_name = secure_filename(file.filename)
                # get file type from file name string
                file_type=file_name.split('.')[1]
                #if path doesnt exist create path
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                # to avoid collision with same filename change file name to uuid
                file_name = str(uuid.uuid4())+'.'+file_type
                # save file in filesystem
                outfile = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                file.save(outfile)
                # 64 pixel genişliğinde kaydet
                Controller.save_image_by_ratio(outfile, 's')
                # 128 pixel genişliğinde kaydet
                Controller.save_image_by_ratio(outfile, 'm')
                file_dict = {'file_name' : file_name, 'title':post_request_args['title'],'description':post_request_args['description'] ,'related_to_field':post_request_args['related_to_field']}
                if post_request_args['related_to_user']:
                    file_dict['related_to_user'] = ObjectId(post_request_args['related_to_user'])
                if post_request_args['related_to_message']:
                    file_dict['related_to_message'] = ObjectId(post_request_args['related_to_message'])
                if post_request_args['related_to_company']:
                    file_dict['related_to_company'] = ObjectId(post_request_args['related_to_company'])
                # create file record in db
                file_record = self.jobs.create(file_dict)
                # check if photo added on damage or embedded damage records
                if file_record.related_to_field and 'photo' in file_record.related_to_field :
                    cont = MessageCont()
                    cont.create_photo_added_history_message(file_record)
                return dumps(loads(file_record.to_json())), 201
        except Exception as e:
            app.logger.error(("***{} post method occurred an error").format(self.__class__.__name__))
            app.logger.exception(e.args)
            return e.args, 500

    @login_required
    def get(self, mongoid=None):
        getRequestArgs = getArgs().parse_args()
        if mongoid:
            return Photo.objects(id=mongoid).first().to_json(), 201
        else:
            request_parser = GetAllRequestParser(Photo, getRequestArgs, None, None)
            # parse arguments and return result
            return request_parser.run()

    @login_required
    def delete(self,mongoid=None):
        if mongoid:
            result = self.jobs.delete(mongoid)
            if result:
                return result, 201
            else:
                return result, 500
        else:
            return False, 500


app.logger.debug("*** RoutePhoto api")
api.add_resource(RoutePhoto,
                 '/api/v1/photo/',
                 '/api/v1/photo/<mongoid>',
                 endpoint='photo',
                 methods=['GET', 'POST', 'PUT', 'DELETE'])
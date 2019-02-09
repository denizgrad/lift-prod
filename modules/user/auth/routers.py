import datetime
import inspect
import re
from functools import wraps

import jwt
from bson.json_util import dumps
from flask import session, request, Response
from flask_restful import Resource
from jwt import DecodeError
from werkzeug.security import check_password_hash

from helpers.http_responses import SoftRestResponse
from modules.permission.models import Permission
from modules.user.controller import user_controller
from resources import app, api
from .controller import ControllerAuth
from ..models import User
from ...helper2 import helper as helper


class auth_router(Resource):
    """
    Extends of flask restfull resource
    :param Resource extended class
    """
    def __init__(self):
        self.jobs = ControllerAuth()
        self.user_controller = user_controller()
        self.logger = self.jobs.logger
        self.help = helper()

    def get(self) -> object:
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return SoftRestResponse.error(
                message='NOT_ACCEPTABLE',
                detail='Kullanıcı adı veya şifre eksik!',
                code=406
            )
        user = User.objects(email=auth.username).first()
        if not user:
            return SoftRestResponse.error(
                message='RECORD_NOT_FOUND',
                detail='Böyle bir kullanıcı bulunmamaktadır!',
                code=404
            )
        if not user.organization.is_enabled:
            return SoftRestResponse.error(
                message='ORG_IS_PASSIVE',
                detail='Firmanız pasif durumdadır',
                code=403
            )
        if check_password_hash(user.password, auth.password):
            token = jwt.encode(
                {'id': str(user.id), 'exp': datetime.datetime.now() + datetime.timedelta(minutes=3600)},
                app.config['SECRET_KEY'])
            message = {'liftnec-token': token.decode('UTF-8'), 'user': user.to_mongo()}
            return SoftRestResponse.single_item(
                item_id=str(user.id),
                item=message,
                document_name='Login',
                created=True
            )
        return SoftRestResponse.error(
            message='WRONG_PASSWORD',
            detail='Kullanıcı adı ve şifreniz uyuşmamaktadır',
            code=403
        )


def findModuleForClass(modules, class_name):
    for module in modules:
        if re.search(module, class_name.split("_")[1], re.IGNORECASE) is not None and re.search(module, class_name.split("_")[1], re.IGNORECASE):
            return module
    return None


def checkPermission(current_user, f):
    try:
        help = helper()
        modules = help.listModules()
        clazz = get_class_that_defined_method(f)
        module_name = findModuleForClass(modules, clazz.__name__)
        if not module_name:
            raise Exception("Module not found")
        permissions = []
        for role in current_user.roles:
            data = Permission.objects(module_name=module_name, organization=current_user.organization, role_name=role)
            permissions = permissions + [ob.to_mongo() for ob in data]

        for permission in permissions:
            for action in permission['action_list']:
                if(module_name == 'user' and f.__name__ == 'put'):
                    return True
                if re.search(f.__name__, action, re.IGNORECASE):
                    return True
        return False
    except Exception as e:
        app.logger.error("*** checkPermission occurred an exception: f: {}\n*ERROR:{}"
                         .format(f, e))
        return True


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'liftnec-token' in request.headers:
            token = request.headers['liftnec-token']

        if not token:
            message = dumps({'message': "Token is missing!"})
            return Response(message, status=401, mimetype='application/json')

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.objects.get(id=data['id'])
            session["current_user_id"] = data['id']
            session["current_org_id"] = str(current_user.organization.id)
            print("request with Organization id =" + session["current_org_id"])
            # TODO:deniz: Burayı çalışabilmek için kapatıyorum. Stock rest erişiminde hata veriyor
            # if not checkPermission(current_user, f):
            #     message = dumps({'message': "Permission is not valid for this action!"})
            #     return Response(message, status=403, mimetype='application/json')

        except DecodeError as e:
            if admin_check():
                return f(*args, **kwargs)
            else:
                message = dumps({'message': "Permission or Token is invalid!"})
                return Response(message, status=401, mimetype='application/json')
        except Exception as e:
            if admin_check():
                return f(*args, **kwargs)
            else:
                message = dumps({'message': "Token is invalid!"})
                return Response(message, status=401, mimetype='application/json')
        return f(*args, **kwargs)
    return decorated


def get_class_that_defined_method(meth):
    if inspect.ismethod(meth):
        print('this is a method')
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
    if inspect.isfunction(meth):
        print('this is a function')
        return getattr(inspect.getmodule(meth),
                       meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
    print('this is neither a function nor a method')
    return None


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if admin_check():
            return f(*args, **kwargs)
        else:
            message = dumps({'message': "Permission or Token is invalid!"})
            return Response(message, status=401, mimetype='application/json')
    return decorated


def admin_check():
    token = None

    if 'liftnec-token' in request.headers:
        token = request.headers['liftnec-token']

    if not token:
        message = dumps({'message': "Token is missing!"})
        return Response(message, status=401, mimetype='application/json')

    if token == "liftnec-admin":
        session["current_user_id"] = "admin"
        session["current_org_id"] = "admin"
        return True
    else:
        return False


api.add_resource(
    auth_router,
    '/login',
    endpoint='api-auth',
    methods=['GET', 'POST']
)
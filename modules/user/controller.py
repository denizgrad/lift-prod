from bson import ObjectId

from abstracts import abstract_resource_controller
from abstracts.abstract_resource_controller import AbstractResourceController
from helpers.http_responses import SoftRestResponse
from mail_conf import send_user_created_by_owner_email
from modules.helper2 import helper
from modules.organization.org_controller import org_controller
from modules.permission.controller import Controller
from .models import User
from ..organization.models import Organization
from ..permission.constants import EnumPermission
from modules.currency.models import Currency
from modules.currency.constants import *
from ..organization.constants import EnumOrganization
from resources import app,bcrypt
import uuid
from flask_login import current_user
import jwt
import datetime
from flask import Response, session, request
from bson.json_util import dumps,loads
from werkzeug.security import generate_password_hash

__all__ = ['user_controller']


class user_controller(AbstractResourceController):
    def __init__(self):
        self.helper = helper()
        self.abstract = super(user_controller, self)
        self.main_model = User
        self.default_kwargs = dict()
        self.cont_permission = Controller()
        app.logger.debug('*** {} class called'.format(self.__class__.__name__))


    def create(self, data):
        """
        Create a new record
        :param data: dict
        :return: dict
        """
        try:
            org_name = data.pop("organizationName")
            firstTime = True
        except Exception as e:
            org_name = None
        try:
            """login korumalı degil metod"""
            control = self.checkLogin()
            firstTime = False
            if control:
                return control
            if session['current_org_id']:
                org_id = session['current_org_id']
            else:
                org_id = data.pop("organizationId")
        except Exception as e:
            org_id = None

        app.logger.debug('*** {}.create method fired'.format(self.__class__.__name__))
        app.logger.debug(data)
        if isinstance(data, dict) is True:
            # Check if company exists on db
            try:
                if org_name:
                    company_record = Organization.objects(name=org_name)

                    if company_record:
                        return SoftRestResponse.error(
                            message='SERVER_ERROR_POST',
                            detail='Firma zaten var.\nKullanıcı kayıdı için firma yöneticiniz ile görüşün',
                            code=500
                        )
                # unpack dict data for User constructor
                elif org_id:
                    company_record = Organization.objects.get(id=org_id)
                    if not company_record:
                        return SoftRestResponse.error(
                            message='SERVER_ERROR_POST',
                            detail='Firma bulunamadı.\nKullanıcı kayıdı için firma yöneticiniz ile görüşün',
                            code=500
                        )
                else:
                    return SoftRestResponse.error(
                        message='SERVER_ERROR_POST',
                        detail='Firma bilgisi zorunludur',
                        code=500
                    )

                email = data.get("email")
                user_records = User.objects(email=email)
                if len(user_records) > 0:
                    return SoftRestResponse.error(
                        message='SERVER_ERROR_POST',
                        detail='Kullanıcı oluşturulamadı.\nKullanıcı email kaydı zaten var',
                        code=500
                    )

                user_to_insert = User(**data)
                # enable user for login
                user_to_insert.is_enabled = True
                if not user_to_insert.password:
                    user_to_insert.password = str(uuid.uuid4())
                # encrypt password field
                hashed_password = generate_password_hash(user_to_insert.password, method='sha256')
                if firstTime:
                    user_to_insert.password = hashed_password
                    user_to_insert.roles = [EnumPermission.FIRMA_ADMIN.value]
                else:
                    # Eğer kullanıcı şirket yöneticisi tarafından
                    # oluşturulmuşsa şifre oluşturması için eşsiz değer oluştur
                    user_to_insert.password = hashed_password
                    user_to_insert.roles = [EnumPermission.SIRKET_CALISANI.value] if not user_to_insert.roles else user_to_insert.roles
                    pass

                if not company_record:
                    # instantiate Company object with Sistem Value
                    company_record = Organization(name=org_name, type=EnumOrganization.SISTEM.value)
                    company_record.save()
                    self.cont_permission.create_default(company_record)

                user_to_insert.organization = company_record
                user_to_insert.save()

                currency = None
                try:
                    currency = Currency.objects.get(code=CURRENCY_TRY)
                except:
                    pass

                if not currency:
                    currency = Currency(
                        code=CURRENCY_TRY,
                        name=CURRENCY_TRY_DESCRIPTION).save()

                company_record._key_currency = currency
                company_record._key_created_user = user_to_insert.pk
                company_record._key_last_modified_user = user_to_insert.pk
                company_record._key_owner_user = user_to_insert.pk
                company_record.save()

                token = jwt.encode(
                    {'id': str(user_to_insert.id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=3600)},
                    app.config['SECRET_KEY'])

                if firstTime:
                    message = {'liftnec-token': token.decode('UTF-8'), 'user': user_to_insert.to_mongo()}
                    return SoftRestResponse.single_item(
                        item_id=str(user_to_insert.id),
                        item=token.decode('UTF-8'),
                        document_name='Login',
                        created=True
                    )
                else:
                    owner = User.objects.get(id=session["current_user_id"])
                    # Eğer kullanıcı şirket yöneticisi tarafından oluşturulmuşsa davetiye bildirimi oluştur
                    send_user_created_by_owner_email(
                        user_to_insert,
                        owner.full_name,
                        'Liftnec Davetiye',
                        token
                    )
                    return SoftRestResponse.single_item(
                        item_id=str(user_to_insert.id),
                        item={'message': 'Kullanıcı yaratıldı, parola oluşturma mail\'i gönderildi'},
                        document_name='User',
                        created=True
                    )
            except KeyError as e:
                app.logger.error("***User org key don't exist")
                app.logger.exception(e)
                return SoftRestResponse.error(
                    message='ORG_KEY_NOT_FOUND',
                    detail='Firma bilgisi zorunludur',
                    code=403
                )
            # if company doesnt exist on db
            except Exception as e:
                app.logger.error('*** {}.create occurred an error'.format(self.__class__.__name__))
                app.logger.exception(e)
                return Response(dumps({'message': e.args}),
                                status=500, mimetype='application/json')

    def update(self, mongoid, data):
        """
        Update a record
        :param mongoId: string | mongoID
        :param data: dict
        :return: dict
        """
        app.logger.debug('*** {}.update method fired with mongoid: {}'.format(self.__class__.__name__, mongoid))
        app.logger.debug("***update user data :"+str(data))
        # set record id as ObjectId
        userId = None
        if mongoid is None or mongoid == 'updatePassword':
            userId = session['current_user_id']
        else:
            userId = ObjectId(mongoid)
        data.update({"updated_by": session['current_user_id']})

        # update user record with data kwargs - convert data to json than dict to ensure bson fields conversion
        if 'password' in data:
            if type(data['password']) is str:
                hashed_password = generate_password_hash(data['password'], method='sha256')
                data.update({'password': hashed_password})
        model_dict = self.main_model.objects().get(id=userId).to_mongo()
        data['_key_last_modified_user'] = self.helper.stringIdToObjectId(session['current_user_id'])
        data['_last_modified_date'] = datetime.datetime.now()
        model_dict["id"] = model_dict["_id"]
        del model_dict["_id"]
        return User.update(**model_dict).save()

    def isAdmin(self):
        return session['current_user_id'] == "admin"

    def checkLogin(self):
        if 'liftnec-token' in request.headers:
            token = request.headers['liftnec-token']

        if not token:
            return SoftRestResponse.error(
                message='TOKEN_NOT_FOUND',
                detail='Oturum bulunamadı!',
                code=401
            )

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.objects.get(id=data['id'])
            session["current_user_id"] = data['id']
            session["current_org_id"] = str(current_user.organization.id)
        except Exception as e:
            return SoftRestResponse.error(
                message='TOKEN_NOT_FOUND',
                detail='Oturum bulunamadı!',
                code=401
            )

    def delete(self, mongoid):
        return self.abstract.delete(mongoid)

    def get(self, get_args):
        return self.abstract.get(get_args)


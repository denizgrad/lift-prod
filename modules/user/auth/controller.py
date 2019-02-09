from resources import app, bcrypt
from modules.user.controller import user_controller
from login_util import UserOb, LoginUtil
from flask_login import logout_user, login_required, login_user
from mail_conf import (
    sendForgetPasswordEmail,
    generateSifreUnuttumNotificationBody
)
import uuid
from ..models import User
from flask import session


class ControllerAuth:
    def __init__(self):
        self.user_ctrl = user_controller()
        self.logger = app.logger
        self.logger.debug('*** {} class called'.format(self.__class__.__name__))

    def create(self, create_data):
        """
        New user data
        :param create_data:
        :return: dict
        """
        return self.user_ctrl.create(create_data)

    def update(self, update_data):
        """
        Update user data
        :param userid: string | ObjectID as string
        :param update_data: dict
        :return: dict
        """
        # return self.user_ctrl.update(update_data)
        return self.update_password_via_uuid(update_data)



    def check_email(self, get_args):
        """
        Check email exists
        :param get_args: dict | email should not be none type
        :return: bool
        """
        if get_args['email'] is None:
            return {"result": "Failed", "detail": "Email key is required"}, 406
        try:
            result = User.objects(email=get_args['email']).first()
            if result:
                return True, 200
        except Exception as e:
            self.logger.error("*** {}.check_email Email Check Error".format(self.__class__.__name__))
            self.logger.exception(e)
            return False, 204
        # not found
        return False, 204
    
    def set_user_api_key(self, get_args):
        """
        Set user api_key
        :param get_args:
        :return:
        """
        self.logger.debug("*** {}.set_user_api_key method fired".format(self.__class__.__name__))
        user_record = User.objects(email=get_args['email']).first()
        self.logger.debug("***Login Check User")
        checkResult = bcrypt.check_password_hash(User.password, get_args["password"])
        self.logger.debug("***Login Check Password Result" + str(checkResult))
        api_key = uuid.uuid4()
        user_record = User.objects(email=User['email'])
        user_record.api_key = str(api_key)
        user_record.save()
        if checkResult:
            return str(api_key), 201
        return None, 500
    
    def forget_password(self, get_args):
        """
        Send password recover email
        :param get_args: dict | email key is required
        :return: string
        """
        self.logger.debug("*** {}.forget_password method fired".format(self.__class__.__name__))
        id = uuid.uuid4()
        try:
            user_record = User.objects.get(email=get_args["email"])
            user_record.password_rec = str(id)
            self.logger.debug('***Forget Password Email to Send :' + get_args["email"])
            link = app.config.get("HOST_NAME") + "passwordRecover/" + str(id)
            sendForgetPasswordEmail(
                [get_args["email"]],
                "Şifre Yenileme",
                generateSifreUnuttumNotificationBody(user_record),
                "QRCROS Şifre Yenileme",
                link
            )
            user_record.save()
            return "Success email has been sent", 201
        except Exception as e:
            self.logger.error("***Exception Forget P. Email Sending")
            self.logger.error(e.args)
            self.logger.error("Exception Forget P. Email Sending***")
            return "Exception email cannot be send", 505

    def update_password_via_uuid(self, put_args):
        """
        Update password with
        :param put_args: dict | email, passwordRec and password keys are required
        :return: None
        """
        self.logger.debug("*** {}.update_password_via_uuid method fired".format(self.__class__.__name__))
        self.logger.debug("*** put_args: {}".format(str(put_args)))
        if "passwordRec" not in put_args\
                or "email" not in put_args\
                or "password" not in put_args:
            return {"result": "Failed", "detail": "passwordRec, password and email are required"}, 406
        email = put_args["email"]
        password = put_args["password"]
        app.logger.debug("***Update Password Email:" + put_args["email"])
        cpass = bcrypt.generate_password_hash(password)
        user_record=User.objects(email=put_args['email'], password_rec=put_args["passwordRec"]).first()
        user_record.password=cpass
        try:
            user_record.save()
            return None, 201
        except Exception as e:
            return {
               "result": "Failed",
               "detail": "{} recovery key not valid for {}".format(put_args["passwordRec"], email)
            }, 406

    def login(self, get_args):
        """
        Check user creadentials and set login session
        :param get_args: dict
        :return:
        """
        try:
            app.logger.debug("***Login Check User" + get_args["email"])
            user_record=User.objects(email=get_args['email']).first()
            if user_record  :
                app.logger.debug("***Login Check User success user found")
                checkResult=bcrypt.check_password_hash(user_record.password, get_args["password"])
                app.logger.debug("***Login Check Password Result"+str(checkResult))
                #if not user["isenabled"]:
                   #flash('Kullanıcınız aktif değildir.Lütfen yöneticiniz ile iletişime geçiniz.')
                if checkResult and user_record.is_enabled:

                    user_ob = UserOb(user_record.id,user_record.email,user_record.first_name,user_record.last_name,user_record.permissions,user_record.is_enabled,user_record.company.id,False)
                    login_user(user_ob, False, True, True)
                    app.logger.debug("***Login Current User")
                    next = get_args['next']
                    if not LoginUtil.is_safe_url(next):
                        return app.abort(400)
                    if next is not None:
                        return {"api_key": user_record.api_key, "url": next}, 201
                    else:
                        firstPath = "/"
                        return {"api_key": user_record.api_key, "url": firstPath}, 201
                elif not user_record.is_enabled:
                    return False, 403
                else:
                    return False,401
            else :
                return False,401
        except Exception as e:
            app.logger.error("****Login Check User Error")
            app.logger.exception(e)
            return False,404

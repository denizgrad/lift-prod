from flask.sessions import SecureCookieSessionInterface
from flask_login import  user_loaded_from_header
from flask import g

from resources import app,login_manager
from login_util import UserOb
from modules.user.models import User


class FlaskLoginCustomization:
    """
    Customization of Flask Login Methods

    :func load_user(user_id):
    :func user_loaded_from_header(user):
    :func load_user_from_request(request):
    """

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        """
        load_user(user_id)-When logged in get User record from database and return user object

        :param user_id:Id of the user which is email
        :return :UserOb object from Class UserOb
        """
        try:
            user_record=User.objects(email=user_id).first()
            app.logger.debug("*** Load User Object :")
            app.logger.debug(user_record)

            userOb=UserOb(user_record.id, user_record.email, user_record.first_name,
                          user_record.last_name, user_record.permissions,
                          user_record.is_enabled, user_record.company.id,False)

        except Exception as e:
            app.logger.debug("***Load User exception : User not found,cannot be loaded")
            app.logger.exception(e)
            return  None
        return userOb

    @staticmethod
    @user_loaded_from_header.connect
    def user_loaded_from_header(user=None):
        """
        user_loaded_from_header(user)-enable log in from header

        :param user:User Object which is not used by default
        :return: Void
        """
        g.login_via_header = True

    @staticmethod
    @login_manager.request_loader
    def load_user_from_request(request):
        """
        load_user_from_request(request)-Get user from http request
        :param request:Http request
        :return: Void
        """
        app.logger.debug('*** load user from request started')
        # first, try to login using the api_key uapprl arg
        api_key = request.args.get('api_key')

        app.logger.debug('*** load user from request api_key1 :' + str(api_key))
        if api_key:
            app.logger.debug('*** Via Url Param Login : ' + api_key)
            try:
                user_record=User.objects(api_key=api_key).first()
                if user_record.is_enabled is True:
                    userOb = UserOb(user_record.id, user_record.email, user_record.first_name,
                                    user_record.last_name, user_record.permissions,
                                    user_record.is_enabled, user_record.company.id,False)
                    app.logger.debug("***userOb")
                    app.logger.debug(userOb)
                    return userOb
            except Exception as e:
                app.logger.error('*** load user from request cannot find user')
                app.logger.exception(e)
                return None




class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""
    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args,
                                                                **kwargs)



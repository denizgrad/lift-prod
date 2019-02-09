from urllib import parse

from flask import request


class LoginUtil:
    @staticmethod
    def is_safe_url(target):
            ref_url = parse.urlparse(request.host_url)
            test_url = parse.urlparse(parse.urljoin(request.host_url, target))
            return test_url.scheme in ('http', 'https') and \
                    ref_url.netloc == test_url.netloc


    @staticmethod
    def checkPermissions(permission,permissions):
            is_contain=False
            for perm in permissions:
                if(perm==permission):
                    is_contain=True

            return is_contain


class UserOb():
    def __init__(self, mongoid, id,firstname,lastname,permissions,enabled,company_id,qr):
        """
        :param id: string | we choosed user email for id
        :param firstname: string
        :param lastname: string
        :param permissions: list
        :param enabled: bool
        :param sms_notification: bool
        :param company_id : mongo id
        :param qr : bool
        """
        self.id = id
        self.__userid = mongoid
        self.__firstname=firstname
        self.__lastname=lastname
        self.__permissions=permissions
        self.__is_enabled=enabled
        self.__company_id=company_id
        self.__qr=qr

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return True
    @is_active.setter
    def set_is_active(self,value):
        self.is_active=value

    @property
    def is_authenticated(self):
        return True
    @is_authenticated.setter
    def set_is_authenticated(self,value):
        self.is_authenticated=value

    @property
    def is_anonymous(self):
        return False
    @is_anonymous.setter
    def set_is_anonymous(self,value):
        self.is_anonymous=value

    @property
    def is_enabled(self):
        return self.__is_enabled
    @is_enabled.setter
    def set_is_enabled(self,value):
        self.__is_enabled=value

    @property
    def firstname(self):
        return self.__firstname
    @firstname.setter
    def set_firstname(self,value):
        self.__firstname=value

    @property
    def lastname(self):
        return self.__lastname

    @lastname.setter
    def set_lastname(self, value):
        self.__lastname = value

    @property
    def permissions(self):
        return self.__permissions
    @permissions.setter
    def set_permissions(self,value):
        self.__permissions=value

    @property
    def sms_notification(self):
        return self.__sms_notification
    @permissions.setter
    def set_sms_notification(self,value):
        self.__sms_notification = value

    @property
    def userid(self):
        return self.__userid
    @userid.setter
    def set_userid(self, value):
        self.__userid = value

    @property
    def company_id(self):
        return self.__company_id

    @company_id.setter
    def company_id(self, value):
        self.__company_id = value

    @property
    def qr(self):
        return self.__qr

    @qr.setter
    def qr(self, value):
        self.__qr = value
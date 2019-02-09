from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_restful import Api
from flask_mail import Mail
from config import ErpConfig
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
import os
from flask_cors import CORS
from mongoengine import connect, register_connection

from register_schedule import ScheduleController


class AppHandler:
    __instance = None

    def __init__(self):
        pass

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = AppHandler()
            cls.__instance.app = Flask(__name__)
            cls.__instance.test = True
        return cls.__instance

    def set_flask_config(self,config_class):
        self.__instance.app.config.from_object(config_class)

    def set_flask_extensions(self):
        CORS(self.__instance.app)
        self.__instance.app.bcrypt = Bcrypt(self.__instance.app)
        self.__instance.app.api = Api(self.__instance.app)
        self.__instance.app.mail = Mail(self.__instance.app)

    def set_mongo_db(self,db_name, db_host):
        if self.__instance.app.config['UNIT_TEST'] :
            self.__instance.app.db = connect('mongoenginetest', host='mongomock://127.0.0.1/')
            self.__instance.app.db.drop_database('mongoenginetest')
        else:
            self.__instance.app.db = connect(db_name, host=db_host)

    def set_flask_login_manager(self):
        login_manager = LoginManager()
        login_manager.login_view = "/user/login"
        login_manager.login_message = None  # "Sayfaya ulaşmak için , giriş yapmalısınız."
        login_manager.login_message_category = "info"
        login_manager.init_app(self.__instance.app)

    def set_log_handlers(self):
        log_path = self.__instance.app.config.get('LOG_PATH', '/log/liftnec/logs/')
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        handler = TimedRotatingFileHandler(log_path + datetime.datetime.now().strftime("%d-%m-%Y") + '.log', when='D',
                                           interval=1)
        handler.setLevel(logging.DEBUG)
        handler.mode = ("w")
        formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        formatter_console = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d}  - %(message)s")
        handler.setFormatter(formatter)
        # file logger
        self.__instance.app.logger.addHandler(handler)
        # console logger
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter_console)
        self.__instance.app.logger.addHandler(console_handler)

    def set_jinja_extensions(self):
        self.__instance.app.jinja_env.add_extension('jinja2.ext.do')

    @staticmethod
    def make_default_conf():
        handler = AppHandler.getInstance()
        handler.set_flask_config(ErpConfig)
        handler.set_flask_extensions()
        handler.set_mongo_db(ErpConfig.MONGO_DBNAME, ErpConfig.MONGO_URI)
        handler.set_flask_login_manager()
        handler.set_log_handlers()
        handler.set_jinja_extensions()
        return handler

handler = AppHandler.make_default_conf()

app = handler.getInstance().app
db = app.db
api = app.api
bcrypt = app.bcrypt
mail = app.mail
login_manager = app.login_manager
global SCHEDULE_CTRL
try:
    SCHEDULE_CTRL = ScheduleController()
except Exception as e:
    app.logger.error("*** main.py SCHEDULE_CTRL occurred an exception when getting instance of scheduleController")
    app.logger.exception(e)





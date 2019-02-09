class ErpConfig(object):
    """
        Flask app config variables
    """
    HOST_NAME = "http://104.248.250.175/"
    PASSWORD_RECOVERY_ENDPOINT = "user/passwordRecovery/?liftnec-token="
    LOG_PATH = "/var/log/otoservis-logs/"
    SECRET_KEY = "liff"

    #[DATABASE]
    DB_CONNECTION = "mongo"
    # MONGO_URI = "104.248.250.175"
    MONGO_URI = "localhost"
    MONGO_PORT = 27017
    MONGO_DBNAME = "liftnec"
    MONGO_CONNECT = True

    #flask-mongoengine
    MONGODB_DB="liftnec"

    #[SMTP]
    MAIL_SERVER = "mail.soft-nec.com"
    MAIL_PORT = 26
    MAIL_USE_TLS = True
    MAIL_USERNAME = "bilgi@soft-nec.com"
    MAIL_PASSWORD = "-R.et9fEu5sc"

    #[SALESFORCE]
    SF_IS_ACTIVE = False
    SF_FAILS_CHECK_LIMIT = 20
    UPLOAD_FOLDER = 'static/photos/'

    APP_DEBUG = False

    # set db to test and at start drop db
    UNIT_TEST = False


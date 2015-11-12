import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # See Flask documentation for description of common settings:
    # http://flask.pocoo.org/docs/0.10/api/
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # Flask-SqlAlchemy settings https://pythonhosted.org/Flask-SQLAlchemy/
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # Flask-Mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'user@domain.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'abc123'

    FTT_MAIL_SUBJECT_PREFIX = '[File Transfer Tool]'
    FTT_MAIL_SENDER = 'File Transfer Tool Admin <user@domain.com>'
    FTT_ADMIN = os.environ.get('FTT_ADMIN')


    DEFAULT_FILE_STORAGE = 'filesystem'
    UPLOADS_FOLDER = os.path.realpath('.') + '/app/static/uploads/'
    FILE_SYSTEM_STORAGE_FILE_VIEW = 'static'

    # CLUSTER is the name of the host/cluster we are using for the application
    CLUSTER = os.environ.get('FTT_CLUSTER') or 'music'
    # PORT is the port number used for the API by the specified CLUSTER
    PORT = 8000
    # CLUSTER_USER is the name of the account used when accessing the API
    CLUSTER_USER = os.environ.get('FTT_CLUSTER_USER') or 'admin'
    # CLUSTER_PWD is the password used when accessing the API
    CLUSTER_PWD = os.environ.get('FTT_CLUSTER_PWD') or 'admin'
    # CLUSTER_FOLDER is the starting folder to use for file uploads for FTT
    CLUSTER_FOLDER = os.environ.get('FTT_CLUSTER_FOLDER')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

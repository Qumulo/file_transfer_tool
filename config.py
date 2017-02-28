import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # The locally mounted path of the uploads folder. 
    # Must be mounted to a qumulo cluster.
    UPLOADS_FOLDER = '<locally-mounted-upload-path>'

    # The full path of the uploads folder on the Qumulo cluster
    CLUSTER_FOLDER = os.environ.get('FTT_CLUSTER_FOLDER') or '<cluster-upload-path>'

    # Qumulo api host, user, and password
    CLUSTER = os.environ.get('FTT_CLUSTER') or '<cluster-host-name>'
    CLUSTER_USER = os.environ.get('FTT_CLUSTER_USER') or '<cluster-api-user>'
    CLUSTER_PWD = os.environ.get('FTT_CLUSTER_PWD') or '<cluster-api-password>'


    # See Flask documentation for description of common settings:
    # http://flask.pocoo.org/docs/0.10/api/
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # Flask-SqlAlchemy settings https://pythonhosted.org/Flask-SQLAlchemy/
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FTT_ADMIN = os.environ.get('FTT_ADMIN')
    DEFAULT_FILE_STORAGE = 'filesystem'
    FILE_SYSTEM_STORAGE_FILE_VIEW = 'static'

    # PORT is the port number used for the API by the specified CLUSTER
    PORT = 8000

    # Flask-Mail settings. Not currently used
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # FTT_MAIL_SUBJECT_PREFIX = '[File Transfer Tool]'
    # FTT_MAIL_SENDER = 'File Transfer Tool Admin <user@domain.com>'

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

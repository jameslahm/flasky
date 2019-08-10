import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.getenv('SECRET_KEY') or "hard to guess"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[FLASKY]'
    FLASKY_MAIL_SENDER = os.getenv('FLASKY_MAIL_SENDER')
    FLASKY_ADMIN = os.getenv('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_POSTS_PER_PAGE=20
    FLASKY_COMMENTS_PER_PAGE=20


    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    ENV='development'
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME') 
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD') 
    SQLALCHEMY_DATABASE_URI = os.path.join('sqlite:///' + basedir +
                                           '/data-dev.sqlite')

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED=False
    SQLALCHEMY_DATABASE_URI = os.path.join('sqlite:///' + basedir +
                                           '/data-test.sqlite')


class ProductionConfig(Config):
    ENV='production'
    SQLALCHEMY_DATABASE_URI = os.path.join('sqlite:///' + basedir +
                                           '/data.sqlite')


config = {
    'development': Development,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': Development
}

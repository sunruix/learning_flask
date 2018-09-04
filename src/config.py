'''
Created on 2018年4月18日

@author: g
'''
import os

basedir = os.path.abspath(os.path.pardir)

class Config():
    SECRET_KEY = 'hard to guess string'

#     SQLALCHEMY_DATABASE_URI = 'mysql://sunrui:ad0801@localhost/test'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
#     SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <icarux@126.com>'
    MAIL_SERVER = 'smtp.126.com'
#     MAIL_PORT = 587    # use default 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'icarux'
    MAIL_PASSWORD = (os.environ.get('USERNAME') + '{:c}'.format(0x40) +
                     str(int(os.environ.get('USERDOMAIN')[-3:]) + 312) +
                     str(int(os.environ.get('USERDOMAIN')[-3:]) - 81))
    FLASKY_ADMIN = 'icarux@126.com'
    FLASKY_POSTS_PER_PAGE = 10
    FLASKY_FOLLOWERS_PER_PAGE = 10
    FLASKY_COMMENTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir + '/db/dev.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir + '/db/test.db'

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }

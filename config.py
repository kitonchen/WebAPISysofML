# coding=utf-8
class Config(object):
    SECRET_KEY = 'ABCD1234'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:chenpidaxi@localhost/webapi'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_BINDS = {
        'users':'mysql://root:chenpidaxi@localhost/webapi',
        'appmeta':'sqlite:///appdata.db'
    }
'''
    def __init__(self,database):
        SQLALCHEMY_DATABASE_URL = 'mysql://root:81123348chenpi@localhost/{dbname}'.format(dbname=database)
'''

config = {
    'DeveConfig': DevelopmentConfig()
}

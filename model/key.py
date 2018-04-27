# coding=utf-8
from DataBase import db


class Key(db.Model):
    __tablename__ = 'api_tokens'
    # id自增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户名加app名字作为主键
    username = db.Column(db.String(16), primary_key=True, nullable=False)
    app_name = db.Column(db.String(16), nullable=False, index=True)
    app_type = db.Column(db.String(16), nullable=False)
    api_key = db.Column(db.String(32), unique=True, nullable=False)
    api_secret = db.Column(db.String(32), nullable=False)

    def __init__(self, name, app, app_type, api_key, api_secret):
        self.username = name
        self.app_name = app
        self.app_type = app_type
        self.api_key = api_key
        self.api_secret = api_secret

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def to_dict(self):
        return dict({'app_name':self.app_name,
                     'api_key':self.api_key,
                     'api_secret':self.api_secret})

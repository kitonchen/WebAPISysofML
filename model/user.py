# coding=utf-8
from flask_login import UserMixin
from DataBase import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    # id自增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 登录账户名，不允许重复
    name = db.Column(db.String(16), unique=True, nullable=False,index=True)
    password = db.Column(db.String(32), nullable=False)
    phone_number = db.Column(db.String(16), unique=True, nullable=True)
    email = db.Column(db.String(32), nullable=False)

    def __init__(self, name, password, phone_number, email):
        self.name = name
        self.password = password
        self.phone_number = phone_number
        self.email = email

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


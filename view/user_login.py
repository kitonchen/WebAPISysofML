# encoding=utf-8

from flask_login import login_user
from flask_login import login_required

from flask import Blueprint
from flask import request
from flask import render_template
from flask import jsonify
from flask import flash
from flask import redirect
from flask import url_for
from flask_login import LoginManager

from DataBase import db
from model import User
from hashlib import md5

login_manager = LoginManager()

# 以user_login.py为根目录，以此类推
user_login = Blueprint('user_login', __name__,
                       template_folder='../templates/user_login',
                       static_folder='../static/user_login')


# 生成md5信息
def getmd5(word):
    m =md5()
    m.update(word)
    return m.hexdigest()


# 从注册表单生成，用户对象
def register_user(form):
    return User(form.get('username'),
                getmd5(form.get('password')),
                form.get('phone_number'),
                form.get('email'))


# 登录页面
@user_login.route('/login', methods=['GET', 'POST'])
def login():
    if "GET" == request.method:
        return render_template('login.html')
    else:

        username = request.form.get('username')
        password = request.form.get('password')
        return jsonify(username, password)


# 注册页面
@user_login.route('/register', methods=['GET', 'POST'])
def register():
    if "GET" == request.method:
        return render_template('register.html')
    else:
        db.session.add(register_user(request.form))
        db.session.commit()
        # TODO :加入一个注册成功的跳转提示
        return  redirect(url_for('user_login.login'))

@user_login.route('/registcheck',methods=['POST'])
def check_user():
    username = request.form.get('username')
    user = User.query.filter_by(name=username).first()
    if user is None:
        return jsonify(True)
    else:
        return jsonify(False)

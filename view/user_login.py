# encoding=utf-8

from flask_login import login_user
from flask_login import login_required
from viewfile import *
from flask import Blueprint
from flask import request
from flask import render_template
from flask import jsonify
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from flask_login import LoginManager
from flask_login import login_user
from DataBase import db
from model import User
from hashlib import md5

login_manager = LoginManager()
login_manager.login_view = "user_login.login"

# 以user_login.py为根目录，以此类推
user_login = Blueprint('user_login', __name__,
                       template_folder='../templates',
                       static_folder='../static/user_login')


# 字符串生成md5信息
def getmd5(word):
    m = md5()
    m.update(word)
    return m.hexdigest()


# 从注册表单生成，用户对象
def register_user(form):
    return User(form.get('username'),
                getmd5(form.get('password')),
                form.get('phone_number'),
                form.get('email'))


# 用户登录验证
def isvalidate_login(form):
    # TODO ：这里的逻辑不好
    if 'username' in form and 'password' in form:
        username = form.get('username')
        password = form.get('password')
        user = User.query.filter_by(name=username).first()
        if user is not None and user.password == getmd5(password):
            # 合法的进行登录
            # TODO：这里记录在线用户加1
            login_user(user, remember=True)
            return True
    return False


@user_login.route('/registcheck', methods=['POST'])
def check_user():
    # 查询用户是否存在
    username = request.form.get('username')
    user = User.query.filter_by(name=username).first()
    if user is None:
        return jsonify(True)
    else:
        return jsonify(False)


# 用户验证的回调函数
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# 登录页面
@user_login.route('/login', methods=['GET', 'POST'])
def login():
    if "GET" == request.method:
        input_user = request.args.get('user')
        return render_template(login_html,username=input_user)
    else:
        if isvalidate_login(request.form):
            return render_template('admin/admin-index.html')
        else:
            # TODO：记得加入修改好的错误文件
            return render_template('admin/admin-404.html')


# 注册页面
@user_login.route('/register', methods=['GET', 'POST'])
def register():
    if "GET" == request.method:
        return render_template(register_html)
    else:
        db.session.add(register_user(request.form))
        db.session.commit()
        # TODO :加入一个注册成功的跳转提示
        flash(u'注册成功', 'successful')
        return  redirect(url_for('user_login.login',user=request.form.get('username')))


# 用户通过代码，命令行登录
@user_login.route('/clogin',methods=['POST'])
def api_login():

    if isvalidate_login(request.form):
        return jsonify({'message':'user login successful',
                        'status':True})
    else:
        return jsonify({'message':'user not found,please register one',
                        'status':False})

# encoding=utf-8

from viewfile import *
from flask import Blueprint, request, render_template
from flask import jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user
from DataBase import db
from model import User
from misson import getmd5

login_manager = LoginManager()
login_manager.login_view = "user_login.login"

# 以user_login.py为根目录，以此类推
user_login = Blueprint('user_login', __name__,
                       template_folder='../templates',
                       static_folder='../static/user_login')


# 从注册表单生成，用户对象
def register_user(form):
    return User(form.get('username'),
                getmd5(form.get('password')),
                form.get('phone_number'),
                form.get('email'))


# 用户登录验证
def isvalidate_login(form):
    if 'username' in form and 'password' in form:
        username = form.get('username')
        password = form.get('password')
        user = User.query.filter_by(name=username).first()
        if user is None or user.password != getmd5(password):
            return False
        else:
            # 合法的进行登录
            # TODO：后期可以添加，记录在线用户加1
            login_user(user, remember=True)
            return True
    else:
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
        if input_user is None:
            input_user = u''
        return render_template(login_html, username=input_user)
    else:
        if isvalidate_login(request.form):
            user = request.form.get('username')
            return redirect(url_for('admin.console', login_user=user))
        else:
            flash(u'用户名或密码错误', 'successful')
        return redirect(url_for('user_login.login'))


# 注册页面
@user_login.route('/register', methods=['GET', 'POST'])
def register():
    if "GET" == request.method:
        return render_template(register_html)
    else:
        db.session.add(register_user(request.form))
        db.session.commit()
        flash(u'注册成功', 'successful')
        return redirect(url_for('user_login.login', user=request.form.get('username')))

    # 注册页面
@user_login.route('/ttyregister', methods=['POST'])
def ttyregister():
    check_resp = check_user()
    if check_resp.data == 'true\n':
        db.session.add(register_user(request.form))
        db.session.commit()
        return jsonify({'message': 'user registe successful',
                        'status': True})
    else:
        return jsonify({'message': 'user has exist',
                        'status': False})





# 用户通过代码，命令行登录
@user_login.route('/ttylogin', methods=['POST'])
def tty_login():
    if isvalidate_login(request.form):
        return jsonify({'message': 'user login successful',
                        'status': True})
    else:
        return jsonify({'message': 'user not found,please register one',
                        'status': False})

# coding=utf-8


from flask import Blueprint
from flask import request
from flask import render_template
from flask import jsonify


view = Blueprint('view', __name__,
                 template_folder='../templates',static_folder='../static' )


# 登录页面
@view.route('/login', methods=['GET', 'POST'])
def login():
    if "GET" == request.method:
        return render_template('/user_login/login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        return jsonify(username, password)


# 注册页面
@view.route('/register', methods=['GET','POST'])
def register():
    if "GET" == request.method:
        return render_template('/user_login/register.html')
    else:
        newuser = request.form.get('username')
        password = request.form.get('password')
        phonenumber = request.form.get('phonenumber')
    return jsonify((newuser, password, phonenumber))

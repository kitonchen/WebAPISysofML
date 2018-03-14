# coding=utf-8
from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import url_for
from flask import request
from flask_login import current_user
from flask_login import logout_user
from user_login import login_required
from user_login import getmd5
from time import time
from model.key import Key
from DataBase import db


admin = Blueprint('admin', __name__,
                  template_folder='../templates',
                  static_folder='../static/admin')


# 获取当前登录的用户名
@admin.route('/get-username')
@login_required
def userinfo():
    return jsonify({'username': current_user.name})


# 修改用户信息
@admin.route('/admin-user')
@login_required
def change_userinfo():
    pass


# 设置
@admin.route('/admin-setting')
@login_required
def setting():
    pass


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_login.login'))


# 登陆后生成api_key
@admin.route('/createkey', methods=['POST'])
@login_required
def create_key():
    appname = request.form.get('appname')
    apptype = request.form.get('apptype')
    # 检查是否有apikey,无则生成apikey和api_sercet,并添加到mysql中
    key = Key.query.filter_by(name=current_user.name,
                             app=appname,
                             apptype=apptype).first()
    if key is None:
        api_key = getmd5(current_user.name + str(appname))
        api_sercet = getmd5(current_user.password+str(time()))
        newkey = Key(current_user.name,
                       appname,
                       apptype,
                       api_key,
                       api_sercet)
        db.session.add(newkey)
        db.session.commit()
        return jsonify({'user': current_user.name,
                    'app': appname,
                    'type': apptype,
                    'api_key': api_key,
                    'api_sercet': api_sercet})
    else:
        return jsonify({'message':'user has exist'})


# 根据用户和应用名字查询apikey
@admin.route('/getapikey/<string:user>/<string:app>')
@login_required
def ret_keysercet(user, app):
    key = Key.query.filter_by(name=user, appname=app).first()
    if not key:
        return jsonify({'error':'user not found'},404)
    else:
        return jsonify(key)

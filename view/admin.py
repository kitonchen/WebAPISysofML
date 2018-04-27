# coding=utf-8
import json
from viewfile import *
from flask import Blueprint, jsonify, redirect
from flask import url_for, request, render_template
from misson import update_userinfo, appname_check
from flask_login import current_user, logout_user, login_required
from user_login import getmd5
from time import time
from model import Key
from DataBase import db
from exception import ApiException

admin = Blueprint('admin', __name__,
                  template_folder='../templates',
                  static_folder='../static/admin')


# 进入控制台
@admin.route('/console')
@login_required
def console():
    user = current_user.name
    # 防止非法访问
    return render_template(admin_index_html, login_user=user)


# 进入帮助页面
@admin.route('/help')
@login_required
def page_help():
    user = current_user.name
    return render_template(admin_help_html, login_user=user)


# 修改用户信息
@admin.route('/admin-user', methods=['GET', 'POST'])
@login_required
def change_userinfo():
    if 'GET' == request.method:
        return render_template(admin_user_html,
                               login_user=current_user.name,
                               old_name=current_user.name,
                               old_email=current_user.email,
                               old_phone=current_user.phone_number)
    else:
        new_name = request.form.get('user-name')
        new_email = request.form.get('user-email')
        new_phone = request.form.get('user-phone')
        update_userinfo(new_name, new_email, new_phone)
        return redirect(url_for('admin.console', login_user=current_user.name))


# 错误信息
@admin.route('/error')
def page_404():
    return render_template(admin_error_html)


# 设置
@admin.route('/admin-setting')
@login_required
def setting():
    pass


# 跳转回首页
@admin.route('/headpage')
@login_required
def head_page():
    user = current_user.name
    return redirect(url_for('admin.console', login_user=user))


# 获取当前登录的用户名
@admin.route('/get-username')
@login_required
def userinfo():
    return jsonify({'username': current_user.name})


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_login.login'))


@admin.route('/appcheck',methods=['POST'])
@login_required
def appnamecheck():
    new_app = request.form.get('appname')
    if appname_check(current_user.name,new_app):
        return jsonify(True)
    else:
        return jsonify(False)

# 登陆后生成api_key
@admin.route('/createkey', methods=['POST'])
@login_required
def createkey():
    new_app = request.form.get('appname')
    new_apptype = request.form.get('apptype')
    api_key = getmd5(current_user.name + str(new_app))
    api_sercet = getmd5(current_user.password+str(time()))
    try:
        db.session.add(Key(current_user.name, new_app, new_apptype, api_key, api_sercet))
        db.session.commit()
        return jsonify({'user': current_user.name, 'app_name': new_app,
                        'type': new_apptype, 'api_key': api_key,
                        'api_secret': api_sercet})
    except Exception as e:
        raise ApiException(message='occur error when creating the api key, please retry')


@admin.route('/deletekey', methods=['POST'])
@login_required
def deletekey():
    delete_app = request.form.get('appname')
    key = Key.query.filter_by(username=current_user.name, app_name=delete_app).first()
    try:
        db.session.delete(key)
        db.session.commit()
        return jsonify({'status':'success'})
    except Exception as e:
        return jsonify({'status':'faile'})


# 根据用户和应用名字查询apikey
@admin.route('/getapikey',methods=['GET'])
@login_required
def ret_keysercet():
    keys = Key.query.filter_by(username=current_user.name).all()
    if keys is None:
        return jsonify({'status': 'error'}, 404)
    else:

        result_set=[json.dumps(key.to_dict()) for key in keys]
        return jsonify({'status': 'success', 'keys': result_set})

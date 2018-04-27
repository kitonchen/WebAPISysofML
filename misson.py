# coding=utf-8
from DataBase import alive_key,db
from flask import request
from flask_login import current_user,logout_user,login_user
from model import Key,User
from functools import wraps
from exception import ApiException
from hashlib import md5

# 字符串生成md5信息
def getmd5(word):
    m = md5()
    m.update(word)
    return m.hexdigest()


# 插入使用活跃的key
def add_hotkey(api_key, api_secret):
    alive_key.set(api_key, api_secret)
    # 设置10分钟过期时间
    alive_key.expire(api_key, 600)


# 包装apikey认证的函数
def key_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'api_key' in request.form and 'api_secret' in request.form:
            post_key = request.form.get('api_key')
            post_secret = request.form.get('api_secret')
            # 查找缓存
            cache_secret = alive_key.get(post_key)
            # 命中
            if cache_secret is not None:
                if cache_secret == post_secret:
                    return func(*args, **kwargs)
                else:
                    raise ApiException('token error',
                                       "api_secret didn't match your api_key",
                                       400)
            else:  # 查找key是否存在数据库中,并检查合法性
                key = Key.query.filter_by(api_key=post_key).first()
                if key is not None:
                    if key.api_secret == post_secret:  # 重新缓存当前key
                        add_hotkey(key.api_key, key.api_secret)
                        return func(*args, **kwargs)
                    else:  # 认证失败
                        raise ApiException('token error',
                                           "api_secret didn't match your api_key",
                                           400)
                else:  # 非法访问
                    raise ApiException('access error',
                                       "Could not find the key:{api_key}".format(api_key=post_key),
                                       400)
        else:  # 参数出错
            raise ApiException('args error',
                               "required api_key and api_secret",
                               400)
    return inner


# 更改用户信息
def update_userinfo(new_name,new_email,new_phone):
    # 已经登录，用户一定存在
    user = User.query.filter_by(name=current_user.name).first()
    user.name = new_name
    user.email = new_email
    user.phone_number = new_phone
    # 以新身份登录
    logout_user()
    login_user(user, remember=True)
    # 提交更改
    db.session.commit()
    return True

def appname_check(user_name,new_appname):
    key = Key.query.filter_by(username=user_name,
                              app_name=new_appname).first()
    if key is None:
        return True
    else:
        return False
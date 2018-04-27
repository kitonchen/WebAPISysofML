# coding:utf-8
from flask import current_app
from flask import Flask
from api import image
from ErrorResponse import error
from view import user_login, login_manager, admin
from config import config
from DataBase import db
from sys import argv
# 设置GPU
# dn_handle.set_gpu(0)

# 需要注册的蓝图集合
blueprints = [user_login, error, image, admin]
# 全局关系数据库操作对象


# 加载网络和元数据
def create_app(app_config, blue_prints):
    app = Flask(__name__)
        # 初始化配置
    app.config.from_object(app_config)
        # 创建数据库表
    with app.app_context():
        db.init_app(app)
        db.create_all()
    login_manager.init_app(app)
        # 注册各蓝图
    for bp in blue_prints:
        app.register_blueprint(bp)
    return app


if __name__ == '__main__':
    apisys = create_app(config['TestConfig'], blueprints)
    # 多线程模式
    apisys.run(host='127.0.0.1', port=12480, threaded=True)

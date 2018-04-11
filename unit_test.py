# coding=utf-8
from flask_testing import TestCase
from flask import url_for
import json
from APIServer import create_app, db, blueprints, config


class FlaskTestCase(TestCase):
    def create_app(self):
        return create_app(config['TeseConfig'], blueprints)

    # 初始化
    def setUp(self):
        self.app = self.create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        # 注册
        resp = self.client.post(
            url_for('user_login.ttyregister'),
            data={'username': u'kiton',
                  'password': u'123456',
                  'email': '1026687121@qq.com',
                  'phone_number': '15622240946'})
        self.assert200(resp)
        res = json.loads(resp.data)
        self.assertEqual(True,res['status'],msg=res['message'])

    def test_login(self):
        # 登录
        self.test_register()
        resp = self.client.post(
            url_for('user_login.tty_login'),
            data={'username': u'kiton',
                  'password': u'123456'})
        self.assert200(resp, message='user login fail')
        res = json.loads(resp.data)
        self.assertEqual(True, res['status'], msg=res['message'])

    def test_createkey(self):
        self.test_login()
        # 生成API-key
        resp = self.client.post(
            url_for('admin.createkey'),
            data={'appname': 'meantest',
                  'apptype': 'image'})
        self.assert200(resp, message='create key fail')
        res = json.loads(resp.data)
        self.assertEqual('kiton',res['user'])
        return res

 #   def craete_keys(self):



if __name__ == '__main__':
    TestCase.main()
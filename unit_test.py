# coding=utf-8
from flask_testing import TestCase
from flask import url_for
import random
import string
import json
import commands
from APIServer import create_app, db, blueprints, config
from multiprocessing import Pool
# 一个任务
def task(cmd):
    output = [float(element) for element in commands.getoutput(cmd).split(",")]
    output = {'time_connect': float(output[0]), 'time_total': float(output[1])}
    return output


class FlaskTestCase(TestCase):

    def create_app(self):
        return create_app(config['TestConfig'], blueprints)

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
        self.assertEqual(True, res['status'], msg=res['message'])

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

    def test_create_key(self):
        self.test_login()
        # 生成API-key
        resp = self.client.post(
            url_for('admin.createkey'),
            data={'appname': 'meantest',
                  'apptype': 'image'})
        self.assert200(resp, message='create key fail')
        res = json.loads(resp.data)
        self.assertEqual('kiton', res['user'])
        return res

    def test_performance(self):
        self.test_login()
        user_num = 4
        repeat = 4000
        request_num = user_num*repeat
        res_list = self.do_performance(10, user_num,repeat)
        # 统计总时间
        total_time = 0.0
        for res in res_list:
            total_time = total_time + res.get().get('time_total')
        print "请求总数：{count}\n" \
              "总花费时间：{time}\n" \
              "并发数:{countsecond}个/秒".format(count = request_num,
                                             time = total_time,
                                             countsecond = int(request_num/total_time))

    def do_performance(self, key_num, user_num=4, repeat=10):
        keys = self.create_keys(key_num)
        res = []
        pool = Pool(user_num)
        # 并发执行
        for i in range(user_num * repeat):
            cmd = self.random_createcmd(keys)
            res.append(pool.apply_async(func=task, args=(cmd,)))
        pool.close()
        pool.join()
        return res

    def create_keys(self,num):
        if not isinstance(num,int):
            return "num must be a integer"
        keys = []
        for i in range(num):
            # 随机生成key
            name = "".join(random.sample(string.ascii_letters,8))
            type = "".join(random.sample(string.ascii_letters,8))
            resp = self.client.post(
                url_for('admin.createkey'),
                data={'appname': name,
                      'apptype': type})
            self.assert200(resp, message='create key fail')
            res = json.loads(resp.data)
            self.assertEqual('kiton', res['user'])
            keys.append(res)
        return keys

    # 随机产生一个curl命令
    def random_createcmd(self, keys):
        choice_key = random.choice(keys)
        command = "curl -o /dev/null -s "
        out_format = "-w %{time_connect},%{time_total} "
        test_url = "http://localhost:12480/image/v1/mean "
        value = "-F 'api_key={key}' -F 'api_secret={secret}' -F 'image={img}'".format(key=choice_key.get('api_key'),
                                                                                      secret=choice_key.get('api_secret'),
                                                                                      img='./darnet/data/dog.jpg')
        return command+out_format+test_url+value

if __name__ == '__main__':
    TestCase.main()

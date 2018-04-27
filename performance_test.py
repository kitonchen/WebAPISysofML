# coding=utf-8
import random, string, json, requests
import commands
from multiprocessing import Pool


# 一个任务
def task(cmd):
    output = [float(element) for element in commands.getoutput(cmd).split(",")]
    output = {'time_connect': float(output[0]), 'time_total': float(output[1])}
    return output


class PerformanceTest():
    # 初始化
    server_url = "http://localhost:12480"
    user = "kiton"
    password = "123456"

    def __init__(self):
        pass

    def register_user(self):
        resp = requests.post(self.server_url+"/ttyregister",
                      data={'username': self.user,
                            'password': self.password,
                            'email': '1026687121@qq.com',
                            'phone_number': '15622240946'})
        return resp

    def login_user(self):
        resp = requests.post(self.server_url + "/ttylogin",
                      data={'username': self.user,
                            'password': self.password})
        return resp

    # 生成key
    def createkeys(self, num):
        if not isinstance(num, int):
            raise TypeError("num must be a interger")
        keys = []
        for key in range(1, num):
            # 随机生成key
            name = "".join(random.sample(string.ascii_letters, 8))
            type = "".join(random.sample(string.ascii_letters, 8))
            url = self.server_url+"/createkey"
            resp = requests.post(
                url,
                data={'appname': name,
                      'apptype': type})
            res = json.loads(resp.request.text)
            keys.append(res)
        return keys

        # 随机产生一个curl命令
    def random_createcmd(self, keys):
        choice_key = random.choice(keys)
        command = "curl -o /dev/null "
        out_format = "-w {time_connect:%{time_connect},time_total:%{time_total}}\n "
        test_url = "http://localhost:12480/image/v1/mean "
        value = "-F 'api_key={key}' -F 'api_secret={secret}' -F 'image={img}'".format(key=choice_key.get('api_key'),
                                                                                      secret=choice_key.get('api_secret'),
                                                                                      img='./darnet/data/dog.jpg')
        return command + out_format + test_url + value

    def do_performance(self, key_num, user_num=4, repeat=10):
        keys = self.createkeys(key_num)
        res = []
        pool = Pool(user_num)
        # 并发执行
        for i in range(user_num * repeat):
            cmd = self.random_createcmd(keys)
            res.append(pool.apply_async(func=task, args=(cmd,)))
        pool.close()
        pool.join()
        return res

    def test_performance(self):
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


if __name__ == "__main__":
    test = PerformanceTest()
    test.register_user()
    test.login_user()
    test.test_performance()
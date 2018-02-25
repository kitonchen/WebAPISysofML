#coding:utf-8

from flask import Flask,jsonify,request,make_response

#设置GPU
#dn_handle.set_gpu(0)
#加载网络和元数据


app = Flask(__name__)





if __name__ == '__main__':

    app.run(host='127.0.0.1',port=12480)

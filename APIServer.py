#coding:utf-8

from flask import Flask
from ImageAPI import image
from ErrorResponse import error
from View import view
#设置GPU
#dn_handle.set_gpu(0)
#加载网络和元数据


app = Flask(__name__)
app.register_blueprint(image)
app.register_blueprint(error)
app.register_blueprint(view)



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=12480)

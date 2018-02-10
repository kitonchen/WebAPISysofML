#coding:utf-8
#导入包
import sys,os
sys.path.append(os.path.join(os.getcwd(),'darknet/python'))
#导入darknet和
import darknet as dn_handle
from flask import Flask,make_response,jsonify

#设置GPU
#dn_handle.set_gpu(0)
#加载网络和元数据
net,meta = dn_handle.init()

app = Flask(__name__)

@app.route('/dectect',methods=['POST'])
def dectect():
    try:
       # date  = request.
    except Exception as e:
        return repr(e),500

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not Found'}),404)

if __name__ == '__main__':
    app.run(debug=True)

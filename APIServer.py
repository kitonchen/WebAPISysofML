#coding:utf-8
#导入包
import sys,os
sys.path.append(os.path.join(os.getcwd(),'darknet'))
#导入darknet和
import darknet as dn_handle
from flask import Flask,jsonify,request,make_response

#设置GPU
#dn_handle.set_gpu(0)
#加载网络和元数据


app = Flask(__name__)



@app.route('/v1/image/dectect',methods=['POST'])
def dectect():
    try:
        post_data = request.files.get('image').read()
        image = dn_handle.data_to_image(post_data)
        res = dn_handle.detect2(net,meta,image)
        return jsonify(res)
    except Exception as e:
        return repr(e),500

if __name__ == '__main__':
    net, meta = dn_handle.init_net()
    app.run(host='127.0.0.1',port=12480)

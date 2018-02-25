#coding:utf-8
#导入包
import sys,os
dir = os.path.join(os.getcwd(),'/darknet')
sys.path.append(os.path.join(os.getcwd(),'darknet'))
#导入darknet和
import darknet as dn_handle
from flask import request,jsonify,Blueprint,abort

image = Blueprint('image',__name__)

net, meta = dn_handle.init_net()

@image.route('/image/dectect',methods=['POST'])
def dectect():
    try:
        if 'image' in request:
            post_data = request.files.get('image').read()
            image = dn_handle.data_to_image(post_data)
            res = dn_handle.detect2(net,meta,image)
            return jsonify(res)
        else:
            abort(400)
    except Exception as e:
        return repr(e),500
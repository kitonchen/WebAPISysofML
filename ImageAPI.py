# coding=utf-8
# 导入darknet
from darknet import darknet as dn_handle
from flask import request
from flask import jsonify
from flask import Blueprint
from flask import abort

image = Blueprint('image', __name__, url_prefix='/image')


net, meta = dn_handle.init_net()


@image.route('/v1/dectect', methods=['POST'])
def dectect():
    try:
        if 'image' in request.files:
            post_data = request.files.get('image').read()
            jpg_data = dn_handle.data_to_image(post_data)
            res = dn_handle.detect2(net, meta, jpg_data)
            return jsonify(res)
        else:
            abort(400)
    except Exception as e:

        return abort(500)

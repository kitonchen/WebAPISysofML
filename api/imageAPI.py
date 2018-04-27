# coding=utf-8
# 导入darknet
import json
from darknet import darknet as dn_handle
from misson import key_required
from flask import request
from flask import jsonify
from flask import Blueprint
from exception import ApiException


image = Blueprint('image', __name__, url_prefix='/image')
# 加载模型
net, meta = dn_handle.init_net()


@image.route('/v1/dectect')

@image.route('/v1/dectect', methods=['POST'])
@key_required
def dectect():
    try:
        if 'image' in request.files:
            post_data = request.files.get('image').read()
            jpg_data = dn_handle.data_to_image(post_data)
            res = dn_handle.detect2(net, meta, jpg_data)
            return jsonify(res)
        else:
            raise ApiException('function dectect call error',
                               'please POST image file ,ex:image=@yourfiles',
                               400)
    except Exception as e:
        raise ApiException('Internal Server Error',
                           'please contact with  server admin',
                           500)


@image.route('/v1/mean',methods=['POST'])
@key_required
def cal_imagemean():
    try:
        if 'image' in request.files:
            files = request.files
            data = files.get('image').read()
            from PIL import Image
            from StringIO import StringIO
            import numpy as np
            # 提取jpg图像的数据
            # 流量大的情况，性能问题来自于并发处理的能力，此时可以使用redis等工具构建消息队列，来批量处理
            # 流量不大的情况，如果使用缓存，对图像数据的序列化和反序列化的时间开销会明显影响性能
            im_jpg = Image.open(StringIO(data))
            img_data = np.asarray(im_jpg, dtype=np.uint8).transpose(2,0,1)
            # 返回图像平均值
            return jsonify({'image':files.get('image').filename,
                     'meanvalue':img_data.mean()})
        else:
            raise ApiException('function imagemean call error',
                               'please POST image file ,ex:image=@yourfiles',
                               400)
    except Exception as e:
        raise ApiException('Internal Server Error',
                           'please contact with  server admin',
                           500)

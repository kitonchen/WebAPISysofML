# coding=utf-8
from flask import make_response
from flask import jsonify
from flask import Blueprint
from flask import request
from exception import ApiException

error = Blueprint('error', __name__)


# 处理api调用的错误,返回为json格式的错误，与视图错误分开来
@error.app_errorhandler(ApiException)
def api_errr(call_error):
    # 接受异常信息，并返回
    return make_response(jsonify({'message': call_error.message,
                                  'detail': call_error.detail}),
                         call_error.status_code)


# 4xx error
@error.app_errorhandler(404)
def not_found():
    if request.method == 'POST':
        return make_response(jsonify({'error': 'Not found'}), 404)


@error.app_errorhandler(400)
def bad_request():
    return make_response(jsonify({'error': 'Bad Response',
                                  'description': 'Resource not found or parameter error'}), 400)


@error.app_errorhandler(500)
def internal_server_error():
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)

from flask import make_response,jsonify,Blueprint

error = Blueprint('error',__name__)

# 4xx error
@error.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}),404)

@error.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error':'Bad Response',
                                  'description':'Resource not found or parameter error'}),400)

@error.error_handler(500)
def internal_server_error(error):
    return make_response(jsonify({'error':'Internal Server Error'}),500)


from flask import make_response,jsonify,Blueprint

error = Blueprint('error',__name__)

@error.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}),404)

@error.error_handler(500)
def internal_server_error(error):
    return make_response(jsonify({'error':'Internal Server Error'}),500)


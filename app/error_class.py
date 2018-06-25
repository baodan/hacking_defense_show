from flask import jsonify, make_response
from app import app
from app.customer_error_class import InvalidMessage
import json


@app.errorhandler(404)
def error_404(error):
    """这个handler可以catch住所有abort(404)以及找不到对应router的处理请求"""
    app.logger.exception(error)
    response = dict(status=404, data="404 Not Found")
    return jsonify(response), 404


@app.errorhandler(InvalidMessage)
def invalid_usage(error):
    data_format = {
        'status': error.status_code,
        'data': error.message
    }
    data = json.dumps(data_format)
    response = make_response(data)
    response.status_code = error.status_code
    response.headers['Content-Type'] = 'application/json'
    return response


@app.errorhandler(Exception)
def error_500(error):
    """这个handler可以catch住所有的abort(500)和raise exeception."""
    app.logger.exception(error)
    response = dict(status=500, data="500 Error")
    return jsonify(response), 500






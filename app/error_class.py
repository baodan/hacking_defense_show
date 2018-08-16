from flask import jsonify, make_response
from app import app
from app.database import db

@app.errorhandler(404)
def error_404(error):
    """这个handler可以catch住所有abort(404)以及找不到对应router的处理请求"""
    app.logger.exception(error)
    db.session.remove()
    response = dict(status=404, message="{}".format(error))
    return jsonify(response), 404


@app.errorhandler(Exception)
def error_500(error):
    """这个handler可以catch住所有的abort(500)和raise exeception."""
    app.logger.exception(error)
    db.session.remove()
    response = dict(status=500, message="{}".format(error))
    return jsonify(response), 500


class InvalidMessage(Exception):
    status_code = 400
    
    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code


@app.errorhandler(InvalidMessage)
def invalid_usage(error):
    db.session.remove()
    response = make_response(error.message)
    response.status_code = error.status_code
    response.heards['Content-Type'] = 'application/json'
    return response



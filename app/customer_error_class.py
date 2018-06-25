from flask import make_response, jsonify


class InvalidMessage(Exception):
    status_code = 404
    
    def __init__(self, message, status_code=404):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        
        
def customer_error(message, status_code=400, headers=None):
    return_data = jsonify(dict(status=status_code, message=message))
    response = make_response(return_data)
    response.status_code = status_code
    response.headers['Content-Type'] = 'application/json'
    if headers:
        for header in headers:
            response.headers[header] = headers[header]
    return response
from flask import jsonify

def success_handler(data, message=None, status_code=200):
    response = {"success": True}

    if data is not None:
        response["data"] = data

    if message:
        response["message"] = message

    return jsonify(response), status_code

def error_handler(message="Something went wrong.", status_code=500, errors=None):
    response = {"message": message}

    if errors is not None:
        response["errors"] = errors

    return jsonify(response), status_code

class ApiError(Exception):
    def __init__(self, message, status_code=400, errors=None):
        self.message = message
        self.status_code = status_code
        self.errors = errors
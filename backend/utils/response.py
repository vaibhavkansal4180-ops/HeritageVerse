from flask import jsonify

def api_response(data=None, message="Success", status_code=200, success=True, errors=None):
    payload = {
        "success": success,
        "message": message,
        "data": data
    }
    if errors is not None:
        payload["errors"] = errors
    return jsonify(payload), status_code

def success_response(data=None, message="Success", status_code=200):
    return api_response(data=data, message=message, status_code=status_code, success=True)

def error_response(message="An error occurred", status_code=400, errors=None):
    return api_response(data=None, message=message, status_code=status_code, success=False, errors=errors)

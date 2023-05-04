import os
from dotenv import load_dotenv
from functools import wraps
from flask import request, jsonify

load_dotenv()

API_KEY = os.environ.get('API_KEY')

def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get("x-api-key"):
            if request.headers.get("x-api-key") == API_KEY:
               return view_function(*args, **kwargs)
            else:
                return jsonify({"error": "Invalid API key"}), 403
        else:
            return jsonify({"error": "No API key provided. Add API key to header 'x-api-key:{{ API_KEY }}' "}), 401

    return decorated_function
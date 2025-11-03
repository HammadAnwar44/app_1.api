from functools import wraps
from flask import request, jsonify
import jwt
import globals

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({"message": "Token missing!"}), 401

        parts = auth_header.split(" ")
        token = parts[1] if len(parts) == 2 and parts[0] == "Bearer" else parts[0]

        # 🔒 Check if token is blacklisted
        if globals.blacklist.find_one({"token": token}):
            return jsonify({"message": "Token has been blacklisted!"}), 401

        try:
            data = jwt.decode(token, globals.SECRET_KEY, algorithms=["HS256"])
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401

        return f(*args, **kwargs)
    return decorated

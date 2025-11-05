from functools import wraps
from flask import request, jsonify
import jwt
import globals

# Use the SAME secret key as your auth.py
SECRET_KEY = globals.SECRET_KEY

# MongoDB collection for blacklisted tokens
blacklist = globals.db.blacklist


def jwt_required(f):
    """
    Decorator to protect routes with JWT authentication.
    Adds `current_user` to the wrapped function.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Authorization header missing"}), 401

        try:
            # Expected format: "Bearer <token>"
            parts = auth_header.split(" ")
            token = parts[1] if len(parts) == 2 else parts[0]

            # Check blacklist
            if blacklist.find_one({"token": token}):
                return jsonify({"error": "Token has been blacklisted. Please log in again."}), 401

            # Decode token
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            current_user = {
                "user": decoded.get("user"),
                "email": decoded.get("email"),
                "admin": decoded.get("admin", False),
                "role": decoded.get("role", "Employee"),
            }

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired! Please log in again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        except Exception as e:
            return jsonify({"error": f"Authentication error: {str(e)}"}), 401

        # Pass current_user to the route
        return f(current_user=current_user, *args, **kwargs)

    return decorated


def admin_required(f):
    """
    Decorator for admin-only routes.
    Requires valid JWT and admin flag set to True.
    """

    @wraps(f)
    @jwt_required
    def decorated(current_user=None, *args, **kwargs):
        if not current_user or not current_user.get("admin", False):
            return jsonify({"error": "Admin access required"}), 403
        return f(current_user=current_user, *args, **kwargs)

    return decorated

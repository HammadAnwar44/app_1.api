from flask import Blueprint, request, jsonify
import jwt
import bcrypt
import datetime
import globals
from decorators import jwt_required

auth_bp = Blueprint("auth_bp", __name__)

users = globals.db.users
blacklist = globals.db.blacklist


# ✅ LOGIN
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}), 400

    user = users.find_one({"username": data["username"]})
    if not user or not bcrypt.checkpw(data["password"].encode('utf-8'), user["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    token_payload = {
        "user": user["username"],
        "email": user["email"],
        "admin": user["admin"],
        "role": user.get("role", "client"),  # optional if you add role later
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }

    token = jwt.encode(token_payload, globals.SECRET_KEY, algorithm="HS256")

    return jsonify({
        "message": f"Welcome back, {user['name']}!",
        "token": token,
        "role": "Admin" if user["admin"] else "Client/Employee",
        "expires_in": "2 hours"
    }), 200


# ✅ LOGOUT → Blacklist Token
@auth_bp.route('/auth/logout', methods=['POST'])
@jwt_required
def logout():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header

    if blacklist.find_one({"token": token}):
        return jsonify({"message": "Token already blacklisted."}), 200

    blacklist.insert_one({
        "token": token,
        "created_at": datetime.datetime.utcnow()
    })

    return jsonify({"message": "Successfully logged out. Token blacklisted."}), 200


# ✅ PROFILE → View Logged-in User Info
@auth_bp.route('/auth/me', methods=['GET'])
@jwt_required
def get_profile():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header

    try:
        data = jwt.decode(token, globals.SECRET_KEY, algorithms=["HS256"])
        return jsonify({
            "username": data["user"],
            "email": data["email"],
            "admin": data["admin"],
            "role": "Admin" if data["admin"] else data.get("role", "Client/Employee")
        }), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


# ✅ ADMIN → View All Blacklisted Tokens
@auth_bp.route('/auth/blacklist', methods=['GET'])
@jwt_required
def view_blacklist():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header

    try:
        data = jwt.decode(token, globals.SECRET_KEY, algorithms=["HS256"])
        if not data.get("admin", False):
            return jsonify({"error": "Only admins can view blacklisted tokens"}), 403

        tokens = list(blacklist.find({}, {"_id": 0, "token": 1, "created_at": 1}))
        return jsonify({
            "count": len(tokens),
            "blacklisted_tokens": tokens
        }), 200

    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

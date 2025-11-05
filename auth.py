from flask import Blueprint, request, jsonify
import jwt
import bcrypt
import datetime
import globals
from decorators import jwt_required


print("AUTH BLUEPRINT LOADED — STATUS = Active")

auth_bp = Blueprint("auth_bp", __name__)

# -------------------------------- MongoDB Collections -----------------------------------

users = globals.db.users
blacklist = globals.db.blacklist


# ------------------------------------- LOGIN --------------------------------------------

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password required"}, 400)

    user = users.find_one({"username": data["username"]})
    if not user or not bcrypt.checkpw(data["password"].encode('utf-8'), user["password"]):
        return jsonify({"error": "Invalid username or password"}, 401)

# -------------------------------- Token Payload ----------------------------------------  

    token_payload = {
        "user": user["username"],
        "email": user["email"],
        "admin": user["admin"],
        "role": user.get("role", "employee"),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }

    token = jwt.encode(token_payload, globals.SECRET_KEY, algorithm="HS256")

    return jsonify({
        "message": f"Welcome back, {user['name']}!",
        "role": "Admin" if user["admin"] else user.get("role", "Employee"),
        "login_time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "token": token
    }, 200)


#----------------------------- LOGOUT (Blacklist Token) -------------------------------- 

@auth_bp.route('/auth/logout', methods=['POST'])
@jwt_required
def logout(current_user=None):
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header

    # Prevent duplicate blacklisting
    if blacklist.find_one({"token": token}):
        return jsonify({"message": "Token already blacklisted."}, 200)

    blacklist.insert_one({
        "token": token,
        "created_at": datetime.datetime.utcnow()
    })

    return jsonify({
        "message": f"Goodbye {current_user['username']}, you’ve been logged out successfully."
    }, 200)


#------------------------------- PROFILE (USER INFO) -----------------------------------

@auth_bp.route('/auth/me', methods=['GET'])
@jwt_required
def get_profile(current_user=None):
    """Return details of the currently logged-in user."""
    try:
        return jsonify({
            "username": current_user["username"],
            "email": current_user["email"],
            "admin": current_user["admin"],
            "role": "Admin" if current_user["admin"] else current_user.get("role", "Employee"),
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to get profile: {str(e)}"}, 500)


# ----------------------------- BLACKLIST (Admin Only) -----------------------------------

@auth_bp.route('/auth/blacklist', methods=['GET'])
@jwt_required
def view_blacklist(current_user=None):
    if not current_user.get("admin", False):
        return jsonify({"error": "Only admins can view blacklisted tokens"}, 403)

    try:
        tokens = list(blacklist.find({}, {"_id": 0, "token": 1, "created_at": 1}))
        return jsonify({
            "count": len(tokens),
            "blacklisted_tokens": tokens
        }, 200)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch blacklist: {str(e)}"}, 500)

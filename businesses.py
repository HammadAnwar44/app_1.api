from flask import Blueprint, jsonify, request
from decorators import jwt_required
from bson import ObjectId
import globals

# --- Blueprint setup ---
businesses_bp = Blueprint("businesses_bp", __name__, url_prefix="/businesses")

# --- MongoDB collection ---
businesses = globals.db.biz


# ==========================================================
# 🧭 TEST ROUTE — WELCOME
# ==========================================================
@businesses_bp.route("/", methods=["GET"])
@jwt_required
def welcome(current_user=None):
    return jsonify({"message": f"Hello {current_user['user']}, welcome to Businesses API"}), 200


# ==========================================================
# 📋 GET ALL BUSINESSES
# ==========================================================
@businesses_bp.route("/all", methods=["GET"])
@jwt_required
def get_all_businesses(current_user=None):
    """List all businesses (paginated, admin or employee)."""
    page_num = request.args.get('pn', default=1, type=int)
    page_size = request.args.get('ps', default=10, type=int)
    page_start = (page_num - 1) * page_size

    query = {}
    if request.args.get("employee_name"):
        query["employee_name"] = request.args.get("employee_name")
    if request.args.get("client_name"):
        query["client_name"] = request.args.get("client_name")
    if request.args.get("status"):
        query["status"] = request.args.get("status")

    try:
        cursor = businesses.find(query).skip(page_start).limit(page_size)
        response = []

        for biz in cursor:
            biz["_id"] = str(biz["_id"])
            response.append(biz)

        return jsonify({
            "page": page_num,
            "count_this_page": len(response),
            "data": response
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================================
# 📄 GET ONE BUSINESS
# ==========================================================
@businesses_bp.route("/<string:biz_id>", methods=["GET"])
@jwt_required
def get_one_business(biz_id, current_user=None):
    try:
        biz = businesses.find_one({"_id": ObjectId(biz_id)})
        if not biz:
            return jsonify({"error": "Business not found"}), 404

        biz["_id"] = str(biz["_id"])
        return jsonify({"message": "Business retrieved", "data": biz}), 200
    except:
        return jsonify({"error": "Invalid ID format"}), 400


# ==========================================================
# 🏢 ADD NEW BUSINESS (ADMIN ONLY)
# ==========================================================
@businesses_bp.route("/", methods=["POST"])
@jwt_required
def add_business(current_user=None):
    if not current_user.get("admin", False):
        return jsonify({"error": "Only admins can add businesses"}), 403

    data = request.get_json() if request.is_json else {}

    required = ["employee_name", "client_name", "site_location", "shift_schedule", "status"]
    if not all(field in data and data[field] for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    new_business = {
        "employee_name": data["employee_name"],
        "client_name": data["client_name"],
        "site_location": data["site_location"],
        "shift_schedule": data["shift_schedule"],
        "status": data["status"],
    }

    result = businesses.insert_one(new_business)
    return jsonify({
        "message": "✅ Business added successfully",
        "business_id": str(result.inserted_id),
        "url": f"/businesses/{result.inserted_id}"
    }), 201


# ==========================================================
# 🧾 UPDATE BUSINESS (ADMIN ONLY)
# ==========================================================
@businesses_bp.route("/<string:biz_id>", methods=["PUT"])
@jwt_required
def update_business(biz_id, current_user=None):
    if not current_user.get("admin", False):
        return jsonify({"error": "Only admins can update businesses"}), 403

    data = request.get_json() or {}
    if not data:
        return jsonify({"error": "Empty request"}), 400

    allowed = [
        "employee_name", "client_name", "site_location", "shift_schedule",
        "incident_report", "status", "response_time", "rating"
    ]
    update_fields = {key: data[key] for key in data if key in allowed}

    try:
        result = businesses.update_one({"_id": ObjectId(biz_id)}, {"$set": update_fields})
        if result.matched_count == 0:
            return jsonify({"error": "Business not found"}), 404

        return jsonify({"message": "✅ Business updated successfully"}), 200
    except:
        return jsonify({"error": "Invalid ID"}), 400


# ==========================================================
# ❌ DELETE BUSINESS (ADMIN ONLY)
# ==========================================================
@businesses_bp.route("/<string:biz_id>", methods=["DELETE"])
@jwt_required
def delete_business(biz_id, current_user=None):
    if not current_user.get("admin", False):
        return jsonify({"error": "Only admins can delete businesses"}), 403

    try:
        result = businesses.delete_one({"_id": ObjectId(biz_id)})

        if result.deleted_count == 0:
            return jsonify({"error": "Business not found"}), 404

        return jsonify({"message": "✅ Business deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Invalid ID format or deletion error: {str(e)}"}), 400

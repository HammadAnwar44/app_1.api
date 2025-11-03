from flask import Blueprint, jsonify, request
from decorators import jwt_required
from bson import ObjectId
import globals

businesses_bp = Blueprint("businesses_bp", __name__)
businesses = globals.biz

# Test Welcome 
@businesses_bp.route('/business', methods=['GET'])
@jwt_required
def welcome():
    user = request.user
    return jsonify({"message": f"Hello {user['user']}, welcome to Businesses API"}), 200


# ✅ Get all businesses
@businesses_bp.route('/business/all', methods=['GET'])
@jwt_required
def get_all_businesses():
    user = request.user  # if you want admin check later

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


# ✅ Get one business
@businesses_bp.route('/business/<string:biz_id>', methods=['GET'])
@jwt_required
def get_one_business(biz_id):
    try:
        biz = businesses.find_one({"_id": ObjectId(biz_id)})
        if not biz:
            return jsonify({"error": "Business not found"}), 404

        biz["_id"] = str(biz["_id"])
        return jsonify({"message": "Business retrieved", "data": biz}), 200
    except:
        return jsonify({"error": "Invalid ID format"}), 400


# ✅ Add business (Admin only)
@businesses_bp.route('/business', methods=['POST'])
@jwt_required
def add_business():
    user = request.user
    if not user['admin']:
        return jsonify({"error": "Only admins can add businesses"}), 403

    data = request.get_json() if request.is_json else request.form

    required = ["employee_name", "client_name", "site_location", "shift_schedule",
                "incident_report", "status", "response_time", "rating", "reviews"]

    if not data or any(field not in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    new_business = {
        "employee_name": data.get("employee_name"),
        "client_name": data.get("client_name"),
        "site_location": data.get("site_location"),
        "shift_schedule": data.get("shift_schedule"),
        "incident_report": data.get("incident_report", "None"),
        "status": data.get("status", "Pending"),
        "response_time": data.get("response_time", "N/A"),
        "rating": data.get("rating", 0),
        "reviews": data.get("reviews", [])
    }

    result = businesses.insert_one(new_business)
    return jsonify({
        "message": "Business added successfully",
        "business_id": str(result.inserted_id),
        "URL": f"/business/{result.inserted_id}"
    }), 201


# ✅ Update business (Admin only)
@businesses_bp.route('/business/<string:biz_id>', methods=['PUT'])
@jwt_required
def update_business(biz_id):
    user = request.user
    if not user['admin']:
        return jsonify({"error": "Only admins can update businesses"}), 403

    data = request.form if not request.is_json else request.get_json()
    if not data:
        return jsonify({"error": "Empty request"}), 400

    allowed = ["employee_name", "client_name", "site_location", "shift_schedule",
               "incident_report", "status", "response_time", "rating"]

    update_fields = {key: data[key] for key in data if key in allowed}

    try:
        result = businesses.update_one({"_id": ObjectId(biz_id)}, {"$set": update_fields})
        if result.matched_count == 0:
            return jsonify({"error": "Business not found"}), 404

        return jsonify({"message": "Business updated successfully"}), 200
    except:
        return jsonify({"error": "Invalid ID"}), 400


# ✅ Delete business (Admin only)
@businesses_bp.route('/business/<string:biz_id>', methods=['DELETE'])
@jwt_required
def delete_business(biz_id):
    user = request.user
    if not user['admin']:
        return jsonify({"error": "Only admins can delete businesses"}), 403

    try:
        result = businesses.delete_one({"_id": ObjectId(biz_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Business not found"}), 404

        return jsonify({"message": "Business deleted successfully"}), 200
    except:
        return jsonify({"error": "Invalid ID format"}), 400

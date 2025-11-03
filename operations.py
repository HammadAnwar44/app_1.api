from flask import Blueprint, jsonify
from decorators import jwt_required
import globals

operations_bp = Blueprint("operations_bp", __name__, url_prefix="/operations")

businesses = globals.biz
users = globals.users


# --- EMPLOYEE OR ADMIN SHIFTS ---
@operations_bp.route('/shifts', methods=['GET'])
@jwt_required
def get_employee_shifts(current_user=None):
    # Allow employees and admins
    if not current_user or (current_user.get("role") != "employee" and not current_user.get("admin", False)):
        return jsonify({"error": "Only employees or admins can view shifts"}), 403

    # Admins see all shifts
    if current_user.get("admin", False):
        all_shifts = list(businesses.find(
            {},
            {"_id": 0, "employee_name": 1, "client_name": 1, "shift_schedule": 1, "status": 1}
        ))
        return jsonify({
            "admin": current_user["user"],
            "total_shifts": len(all_shifts),
            "shifts": all_shifts
        }), 200

    # Employees see only their own shifts
    employee_name = current_user["user"]
    employee_shifts = list(businesses.find(
        {"employee_name": {"$regex": employee_name, "$options": "i"}},
        {"_id": 0, "employee_name": 1, "client_name": 1, "shift_schedule": 1, "status": 1}
    ))

    if not employee_shifts:
        return jsonify({"message": f"No shifts found for {employee_name}"}), 200

    return jsonify({
        "employee": employee_name,
        "shift_count": len(employee_shifts),
        "shifts": employee_shifts
    }), 200


# --- ADMIN REPORTS ---
@operations_bp.route('/reports', methods=['GET'])
@jwt_required
def admin_reports(current_user=None):
    if not current_user.get("admin", False):
        return jsonify({"error": "Admins only"}), 403

    total_users = users.count_documents({})
    total_clients = users.count_documents({"role": "client"})
    total_employees = users.count_documents({"role": "employee"})
    total_businesses = businesses.count_documents({})

    total_reviews = 0
    for b in businesses.find({}, {"reviews": 1}):
        if "reviews" in b:
            total_reviews += len(b["reviews"])

    return jsonify({
        "generated_by": current_user["user"],
        "total_users": total_users,
        "clients": total_clients,
        "employees": total_employees,
        "businesses": total_businesses,
        "total_reviews": total_reviews,
        "message": "📊 Admin system report generated successfully!"
    }), 200

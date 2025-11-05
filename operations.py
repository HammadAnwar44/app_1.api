from flask import Blueprint, jsonify, request
from decorators import jwt_required
import globals
import datetime

# Debug print to confirm import
print("🟢 operations.py LOADED — Flask can see me!")

# -----------------------------------------------------
# Blueprint setup
# -----------------------------------------------------
operations_bp = Blueprint("operations_bp", __name__, url_prefix="/operations")

# MongoDB collection
businesses = globals.db.biz


# =====================================================
# 🔍 HEALTH CHECK
# =====================================================
@operations_bp.route("/ping", methods=["GET"])
def ping():
    """Simple endpoint to confirm operations blueprint is active."""
    print("✅ /operations/ping hit")
    return jsonify({"message": "Operations blueprint alive and healthy"}), 200


# =====================================================
# 👀 EMPLOYEE — VIEW OWN SHIFTS
# =====================================================
@operations_bp.route("/myshifts", methods=["GET"])
@jwt_required
def get_employee_shifts(current_user=None):
    """
    Employees can view their assigned shifts.
    Admins should use /businesses/all instead.
    """
    print("📡 /operations/myshifts hit")

    # Prevent admin from accessing this
    if current_user.get("admin", False):
        return jsonify({"error": "Admins should use /businesses/all to view all shifts"}), 403

    employee_name = current_user.get("user") or current_user.get("username")
    if not employee_name:
        return jsonify({"error": "Employee name missing in token"}), 400

    # Find shifts assigned to employee
    shifts = list(
        businesses.find(
            {"employee_name": {"$regex": employee_name, "$options": "i"}},

            {
                "_id": 0,
                "employee_name": 1,
                "client_name": 1,
                "site_location": 1,
                "shift_schedule": 1,
                "status": 1,
            },
        )
    )

    if not shifts:
        print(f"⚠️ No shifts found for {employee_name}")
        return jsonify({"message": f"No shifts found for '{employee_name}'"}), 200

    print(f"✅ {len(shifts)} shifts found for {employee_name}")
    return jsonify(
        {
            "employee": employee_name,
            "total_shifts": len(shifts),
            "assigned_shifts": shifts,
        }
    ), 200


# =====================================================
# 🧾 EMPLOYEE — SUBMIT DAILY REPORT
# =====================================================
@operations_bp.route("/report", methods=["POST"])
@jwt_required
def submit_daily_report(current_user=None):
    """
    Employees submit daily report for a specific client.
    Example:
    {
        "client_name": "Tesco Express",
        "report_text": "All clear. CCTV checked. No issues."
    }
    """
    print("📡 /operations/report hit")

    # Admins not allowed to post employee reports
    if current_user.get("admin", False):
        return jsonify({"error": "Admins cannot submit employee reports"}), 403

    data = request.get_json() or {}
    if not data.get("client_name") or not data.get("report_text"):
        return jsonify({"error": "client_name and report_text are required"}), 400

    employee_name = current_user.get("user") or current_user.get("username")
    client_name = data["client_name"].strip()

    report_entry = {
        "employee_name": employee_name,
        "report_text": data["report_text"],
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Add report to matching client's business record
    result = businesses.update_one(
        {"client_name": {"$regex": f"^{client_name}$", "$options": "i"}},
        {"$push": {"incident_reports": report_entry}},
        upsert=False,
    )

    if result.matched_count == 0:
        print(f"❌ No client found for {client_name}")
        return jsonify({"error": f"No matching client found for '{client_name}'"}), 404

    print(f"✅ Report submitted by {employee_name} for {client_name}")
    return jsonify(
        {
            "message": "✅ Report submitted successfully",
            "client_name": client_name,
            "submitted_by": employee_name,
            "timestamp": report_entry["timestamp"],
        }
    ), 201


# =====================================================
# 🧠 DEBUG ROUTE — JUST TO VERIFY BLUEPRINT WORKS
# =====================================================
@operations_bp.route("/test", methods=["GET"])
def test_ops():
    """Use this in browser or Postman to confirm /operations works."""
    print("✅ /operations/test hit successfully")
    return jsonify({"message": "Operations blueprint responding OK"}), 200

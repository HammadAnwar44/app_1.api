from flask import Blueprint, request, jsonify
from bson import ObjectId
import globals, datetime, uuid

reviews_bp = Blueprint("reviews_bp", __name__, url_prefix="/reviews")

# MongoDB collection
businesses = globals.db.biz

# ==========================================================
# 💬 ADD REVIEW (PUBLIC — NO LOGIN REQUIRED)
# ==========================================================
@reviews_bp.route("/", methods=["POST"])
def add_review():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    required = ["client_name", "controller", "review", "rating"]
    if not all(field in data for field in required):
        return jsonify({"error": f"Missing required fields: {', '.join(required)}"}), 400

    client_name = data["client_name"].strip()
    controller = data["controller"].strip()

    # ✅ Normalize name for safer matching
    existing_business = businesses.find_one(
        {"client_name": {"$regex": f"^{client_name}$", "$options": "i"}}
    )

    if not existing_business:
        # 🆕 Auto-create new business entry if missing
        new_business = {
            "client_name": client_name,
            "employee_name": controller,  # optional for new records
            "site_location": "N/A",
            "shift_schedule": "N/A",
            "status": "Pending Review",
            "reviews": [],
            "created_at": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        }
        businesses.insert_one(new_business)
        existing_business = new_business

    # ✅ Create review object
    new_review = {
        "review_id": str(uuid.uuid4()),
        "controller": controller,
        "review": data["review"],
        "rating": int(data["rating"]),
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # ✅ Add review to the correct business
    businesses.update_one(
        {"client_name": {"$regex": f"^{client_name}$", "$options": "i"}},
        {"$push": {"reviews": new_review}}
    )

    return jsonify({
        "message": "✅ Review added successfully!",
        "client_name": client_name,
        "review": new_review
    }), 201


# ==========================================================
# 📋 VIEW REVIEWS FOR A CLIENT (PUBLIC)
# ==========================================================
@reviews_bp.route("/<string:client_name>", methods=["GET"])
def get_reviews(client_name):
    """Retrieve all reviews for a specific client."""
    client_name = client_name.strip()

    business = businesses.find_one(
        {"client_name": {"$regex": f"^{client_name}$", "$options": "i"}},
        {"_id": 0, "client_name": 1, "reviews": 1}
    )

    if not business:
        return jsonify({"error": f"No reviews found for client '{client_name}'"}), 404

    reviews = business.get("reviews", [])
    if not reviews:
        return jsonify({"message": f"✅ Client '{client_name}' has no reviews yet."}), 200

    return jsonify({
        "client_name": business["client_name"],
        "total_reviews": len(reviews),
        "reviews": reviews
    }), 200

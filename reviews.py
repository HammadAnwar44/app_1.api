from flask import Blueprint, request, jsonify
from bson import ObjectId
import globals, uuid, datetime

reviews_bp = Blueprint('reviews_bp', __name__, url_prefix="/reviews")
businesses = globals.biz


# --- ADD REVIEW (No ID Required) ---
@reviews_bp.route('', methods=['POST'])
def add_review_no_id():
    data = request.get_json()

    if not data or "client_name" not in data or "review" not in data or "rating" not in data:
        return jsonify({"error": "Please include 'client_name', 'review', and 'rating'."}), 400

    # Try to find the business by client_name
    business = businesses.find_one({"client_name": {"$regex": f"^{data['client_name']}$", "$options": "i"}})

    if not business:
        return jsonify({"error": f"No business found with client name '{data['client_name']}'"}), 404

    review = {
        "_id": str(uuid.uuid4()),
        "controller": data.get("controller", "Anonymous"),
        "review": data["review"],
        "rating": float(data["rating"]),
        "created_at": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }

    businesses.update_one(
        {"_id": business["_id"]},
        {"$push": {"reviews": review}}
    )

    # Update average rating
    biz = businesses.find_one({"_id": business["_id"]}, {"reviews": 1})
    if biz and "reviews" in biz and biz["reviews"]:
        avg_rating = sum(float(r["rating"]) for r in biz["reviews"]) / len(biz["reviews"])
        businesses.update_one({"_id": business["_id"]}, {"$set": {"rating": round(avg_rating, 1)}})

    return jsonify({
        "message": f"✅ Review added successfully for {data['client_name']}!",
        "review_id": review["_id"],
        "rating": review["rating"]
    }), 201


# --- GET ALL REVIEWS FOR A CLIENT ---
@reviews_bp.route('/<string:client_name>', methods=['GET'])
def get_reviews_by_client(client_name):
    biz = businesses.find_one({"client_name": {"$regex": f"^{client_name}$", "$options": "i"}}, {"reviews": 1, "client_name": 1})
    if not biz:
        return jsonify({"error": "Business not found."}), 404

    reviews = biz.get("reviews", [])
    return jsonify({
        "client_name": biz.get("client_name", "N/A"),
        "total_reviews": len(reviews),
        "reviews": reviews
    }), 200

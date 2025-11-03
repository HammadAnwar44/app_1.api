from flask import Blueprint, jsonify

home_bp = Blueprint("home_bp", __name__)

@home_bp.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "✅ Nearby Services Security API Running Successfully",
        "author": "Hammad Anwar",
        "project": "Security Workforce & Client Management System",
        "endpoints": {
            "auth_login": "/login (Basic Auth)",
            "business_data": "/business",
            "operations_data": "/operations",
            "reviews_system": "/reviews"
        },
        "usage_note": "Use Postman to login and get your JWT token to access all protected APIs."
    }), 200

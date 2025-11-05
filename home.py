from flask import Blueprint, jsonify

home_bp = Blueprint("home_bp", __name__)

@home_bp.route('/', methods=['GET'])
def home():
    return jsonify({
        "company": "Nearby Services LTD",
        "description": "A security company providing professional security services across the UK, with a strong presence in London.",
        "project": "Security Workforce & Client Management System",
        "contact": {
            "email": "contact@nearbyservices.co.uk",
            "phone": "07511817385",
            "office_location": "150 Oxford Street, Central London, W1D 1NB"
        },
        "endpoints": {
            "reviews_system": "/reviews"
        }
    }), 200

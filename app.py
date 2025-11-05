from flask import Flask

from blueprints.auth.auth import auth_bp
from blueprints.businesses.businesses import businesses_bp
from blueprints.reviews.reviews import reviews_bp
from blueprints.home.home import home_bp
from blueprints.operations.operations import operations_bp  # operations

import globals


def create_app():
    app = Flask(__name__)

    # Register all blueprints (order doesn’t matter)
    app.register_blueprint(auth_bp)
    app.register_blueprint(businesses_bp)
    app.register_blueprint(operations_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(home_bp)

    # Startup confirmation
    print("\n🚀 Flask app started! Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"   • {rule}")
    print()

    return app


if __name__ == "__main__":
    app = create_app()
    # Full restart on changes (helps ensure fresh imports)
    app.run(debug=True, use_reloader=True)

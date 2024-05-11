from flask import Flask, g
from flask_pymongo import PyMongo
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize MongoDB
    mongo = PyMongo(app)

    # Attach MongoDB to application context
    @app.before_request
    def set_mongo():
        g.mongo = mongo

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("HealthMonitoringAPI")

    # Register blueprints from routes folder
    from .routes.user_routes import user_bp
    from .routes.device_routes import device_bp
    from .routes.patient_routes import patient_bp
    from .routes.routes import general_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(device_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(general_bp)

    return app, mongo


import sqlite3   #data storage
from flask import Flask, request, make_response, jsonify, send_from_directory   #API
from jinja2 import Template  
import redis   #caching
from celery import Celery   #batch jobs
from backend.application.models import db, User, Admin, ServiceProfessional, Customer, Service, ServiceRequest, Reviews, Role, BlockedUsers
from backend.application.database import db
from backend.application.config import LocalDevelopmentConfig
from backend.application.auth import init_security
from flask_security import auth_required, roles_required, current_user, hash_password
from backend.application.routes import admin, auth, api as services_blueprint
from backend.application.resources import api, initialize_routes
from flask_cors import CORS
import os
import logging
from backend.application.celery_init import celery_init_app
from backend.application.cache_init import cache_init_app
from celery.schedules import crontab



# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a global app instance
app = Flask(__name__)
# Create a global celery_app instance - this is what the worker will import
celery_app = None

# Initialize Flask app
def create_app():
    global app, celery_app
    
    # Configure static files
    app.static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'))
    app.template_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'))
    
    # Log directory paths for debugging
    logger.info(f"Static folder: {app.static_folder}")
    logger.info(f"Template folder: {app.template_folder}")
    
    if not os.path.exists(app.static_folder):
        logger.error(f"Static folder does not exist: {app.static_folder}")
        os.makedirs(app.static_folder, exist_ok=True)
    
    CORS(app, resources={
             r"/*": {
                 "origins": ["http://localhost:8081", "http://192.168.1.2:8081"],
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authentication-Token", "Accept", "Authorization"],
                 "expose_headers": ["Content-Type", "Authentication-Token", "Authorization"],
                 "supports_credentials": True
             }
         },
         supports_credentials=True)

    # Configure app
    app.config.from_object(LocalDevelopmentConfig)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
    app.config['SECRET_KEY'] = 'the_secret_key'  # Change this in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Redis cache
    cache = cache_init_app(app)
    
    with app.app_context():
        db.create_all()
        init_security(app)
    
    # Register blueprints with URL prefixes
    app.register_blueprint(admin, url_prefix='/api/admin')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(services_blueprint, url_prefix='/api')
    # app.register_blueprint(main)  # Register main blueprint with no prefix
    
    # Initialize Flask-RESTful API
    api.init_app(app)
    initialize_routes(api)
    
    # Initialize Celery
    celery_app = celery_init_app(app)
    # Celery.autodiscover_tasks(self)
    
    # Serve Vue frontend
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_vue(path):
        if path and (path.startswith('api/') or path.startswith('auth/')):
            return jsonify({"error": "Not found"}), 404
            
        try:
            # First try to serve the exact path
            if path and os.path.exists(os.path.join(app.static_folder, path)):
                return send_from_directory(app.static_folder, path)
            
            # Then try to serve index.html
            return send_from_directory(app.static_folder, 'index.html')
        except Exception as e:
            logger.error(f"Error serving file: {str(e)}")
            return jsonify({"error": "Not found"}), 404
    
    # Add CORS headers to all responses
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        allowed_origins = ['http://localhost:8081', 'http://192.168.1.2:8081']
        if origin in allowed_origins:
            response.headers.add('Access-Control-Allow-Origin', origin)
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authentication-Token,Accept,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Expose-Headers', 'Authentication-Token,Authorization')
        return response
    
    # @celery.on_after_finalize.connect

    # Handle OPTIONS requests
    @app.route('/', defaults={'path': ''}, methods=['OPTIONS'])
    @app.route('/<path:path>', methods=['OPTIONS'])
    def handle_options(path):
        response = make_response()
        origin = request.headers.get('Origin')
        allowed_origins = ['http://localhost:8081', 'http://192.168.1.2:8081']
        if origin in allowed_origins:
            response.headers.add('Access-Control-Allow-Origin', origin)
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authentication-Token,Accept,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Expose-Headers', 'Authentication-Token,Authorization')
        return response
    
    # @celery.on_after_finalize.connect
    
    # Add error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Internal server error"}), 500

    # protected routes
    @app.route('/api/admin/dashboard')
    @auth_required()
    @roles_required('admin')
    def admin_dashboard():
        return jsonify({"message": "Welcome to Admin Dashboard"})

    @app.route('/api/professional/dashboard')
    @auth_required()
    @roles_required('professional')
    def professional_dashboard():
        return jsonify({"message": "Welcome to Professional Dashboard"})

    @app.route('/api/customer/dashboard')
    @auth_required()
    @roles_required('customer')
    def customer_dashboard():
        return jsonify({"message": "Welcome to Customer Dashboard"})

    return app


    
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True, port=8080)
else:
    # When imported by the Celery worker, initialize the app and celery
    app = create_app()
    # Log that celery is initialized
    logger.info("Celery app initialized and available as app:celery_app")





import sqlite3   #data storage
from flask import Flask, request, jsonify   #API
from jinja2 import Template  
import redis   #caching
from celery import Celery   #batch jobs
from application.models import db, User, Admin, ServiceProfessional, Customer, Service, ServiceRequest, Reviews,Role
from application.database import db
from application.config import LocalDevelopmentConfig
from application.auth import init_security
from flask_security import auth_required, roles_required, current_user, hash_password
from application.routes import admin


# Initialize Flask app
def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    
    # Security configurations
    # app.config['SECURITY_PASSWORD_SALT'] = 'your-salt-here'
    # app.config['SECRET_KEY'] = 'your-secret-key-here'
    # app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
    # app.config['SECURITY_TOKEN_MAX_AGE'] = 86400
    # app.config['SECURITY_TRACKABLE'] = True
    # app.config['SECURITY_REGISTERABLE'] = True
    # app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
    # app.config['SECURITY_USERNAME_ENABLE'] = True
    
    db.init_app(app) # Initialize database with flask application
    
    with app.app_context():
        # Drop all tables and recreate them
        # db.drop_all()
        db.create_all()
        init_security(app) 

    # Register blueprints
    app.register_blueprint(admin)

    # protected routes
    @app.route('/admin/dashboard')
    @auth_required()
    @roles_required('admin')
    def admin_dashboard():
        return jsonify({"message": "Welcome to Admin Dashboard"})

    @app.route('/professional/dashboard')
    @auth_required()
    @roles_required('professional')
    def professional_dashboard():
        return jsonify({"message": "Welcome to Professional Dashboard"})

    @app.route('/customer/dashboard')
    @auth_required()
    @roles_required('customer')
    def customer_dashboard():
        return jsonify({"message": "Welcome to Customer Dashboard"})

    return app

# Routes and other application logic can be added here

app = create_app()    

if __name__ == '__main__':
    app.run(debug=True,port=8080)




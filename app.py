import sqlite3   #data storage
from flask import Flask, request, jsonify   #API
from jinja2 import Template  
import redis   #caching
from celery import Celery   #batch jobs
from application.models import db, User, Admin, ServiceProfessional, Customer, Service, ServiceRequest, Reviews,Role
from application.database import db
from application.config import LocalDevelopmentConfig
from application.auth import init_security
from flask_security import auth_required, roles_required, current_user


# Initialize Flask app
def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    
    # Add these required Flask-Security configurations
    app.config['SECURITY_PASSWORD_SALT'] = 'your-salt-here'  # Change this!
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this!
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
    app.config['SECURITY_TOKEN_MAX_AGE'] = 86400  # 24 hours
    app.config['SECURITY_TRACKABLE'] = True
    
    db.init_app(app)
    init_security(app)

    with app.app_context():
        db.create_all()
        
    # Example protected routes
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
app=create_app()
if __name__ == '__main__':
    app.run()




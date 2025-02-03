import sqlite3   #data storage
from flask import Flask, request, jsonify   #API
from jinja2 import Template  
import redis   #caching
from celery import Celery   #batch jobs
from application.models import db, User, Admin, ServiceProfessional, Customer, Service, ServiceRequest, Reviews

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household_services.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

# Create tables programmatically
with app.app_context():
    db.create_all()

# Routes and other application logic can be added here

if __name__ == '__main__':
    app.run(debug=True)




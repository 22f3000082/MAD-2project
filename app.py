import sqlite3   #data storage
from flask import Flask, request, jsonify   #API
from jinja2 import Template  
import redis   #caching
from celery import Celery   #batch jobs
from application.models import db, User, Admin, ServiceProfessional, Customer, Service, ServiceRequest, Reviews
from application.database import db
from application.config import LocalDevelopmentConfig
from flask_security import Security, SQLAlchemyUserDatastore , Security

# Initialize Flask app
def create_app():
 app = Flask(__name__)
 app.config.from_object(LocalDevelopmentConfig)
 db.init_app(app)
 datastore=SQLAlchemyUserDatastore(db,User,Role)

# # Configure SQLite database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household_services.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Initialize SQLAlchemy with the app
# db.init_app(app)

# Create tables programmatically
 with app.app_context():

    db.create_all()

# Routes and other application logic can be added here

if __name__ == '__main__':
    app.run(debug=True)




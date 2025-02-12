# from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin,RoleMixin
# # Initialize SQLAlchemy
# db = SQLAlchemy()
from application.database import db

# Define the User table (base class for Admin, ServiceProfessional, and Customer)
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    active = db.Column(db.Boolean, default=True)
    is_blocked = db.Column(db.Boolean, default=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default='')
    
    # Flask-Security tracking fields
    last_login_at = db.Column(db.DateTime, nullable=True)
    current_login_at = db.Column(db.DateTime, nullable=True)
    last_login_ip = db.Column(db.String(100), nullable=True)
    current_login_ip = db.Column(db.String(100), nullable=True)
    login_count = db.Column(db.Integer, default=0)
    
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))

# Admin table (inherits from User)
class Admin(User):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

# Service Professional table (inherits from User)
class ServiceProfessional(User):
    __tablename__ = 'service_professional'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    service_type = db.Column(db.String(80), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)  # Admin approval status
    __mapper_args__ = {
        'polymorphic_identity': 'professional'
    }

# Customer table (inherits from User)
class Customer(User):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'customer'
    }

# Service table
class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    created_by_admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

# Service Request table
class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professional.id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'rejected', 'closed'
    pin_code = db.Column(db.String(10), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

# Reviews table
class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
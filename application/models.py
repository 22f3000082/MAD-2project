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
    name = db.Column(db.String(80), nullable=True)  # Changed from 'name' to 'display_name'
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
    
    # Admin specific fields
    # last_login_ip = db.Column(db.String(100))
    # login_history = db.Column(db.JSON, nullable=True)  # Store login timestamps and IPs
    # actions_log = db.Column(db.JSON, nullable=True)    # Track admin actions
    
    # Relationships
    created_services = db.relationship('Service', backref='admin', lazy=True)
    approved_professionals = db.relationship('ServiceProfessional', 
                                          backref='approved_by',
                                          lazy=True,
                                          foreign_keys='ServiceProfessional.approved_by_id')
    blocked_users = db.relationship('User',
                                  secondary='blocked_users',
                                  backref=db.backref('blocked_by', lazy=True))

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def approve_professional(self, professional):
        professional.is_approved = True
        professional.approved_by_id = self.id
        professional.approval_date = db.func.current_timestamp()
        db.session.commit()
    
    def block_user(self, user, reason):
        user.is_blocked = True
        user.blocked_at = db.func.current_timestamp()
        user.block_reason = reason
        db.session.commit()
    
    def unblock_user(self, user):
        user.is_blocked = False
        user.unblocked_at = db.func.current_timestamp()
        db.session.commit()
    
    def create_service(self, name, base_price, description=None):
        service = Service(
            name=name,
            base_price=base_price,
            description=description,
            created_by_admin_id=self.id
        )
        db.session.add(service)
        db.session.commit()
        return service

# Add a table to track blocked users
class BlockedUsers(db.Model):
    __tablename__ = 'blocked_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    block_reason = db.Column(db.String(255), nullable=False)
    blocked_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    unblocked_at = db.Column(db.DateTime, nullable=True)

# Update Service model to include more fields
class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    base_price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)  # in minutes
    category = db.Column(db.String(50), nullable=False)  # e.g., 'Plumbing', 'Electrical', 'AC'
    
    # Admin who created/manages this service
    created_by_admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    
    # Service status
    is_active = db.Column(db.Boolean, default=True)
    availability = db.Column(db.String(20), default='available')  # 'available', 'unavailable', 'coming_soon'
    
    # Service details
    min_booking_hours = db.Column(db.Integer, default=1)
    max_booking_hours = db.Column(db.Integer, default=8)
    cancellation_policy = db.Column(db.Text, nullable=True)
    
    # Relationships
    service_requests = db.relationship('ServiceRequest', backref='service', lazy=True)
    professionals = db.relationship('ServiceProfessional', 
                                  secondary='professional_services',
                                  backref=db.backref('services', lazy=True))

# Update ServiceProfessional model to include approval details
class ServiceProfessional(User):
    __tablename__ = 'service_professional'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    professional_name = db.Column(db.String(80), nullable=False)  # Changed from 'name' to 'professional_name'
    description = db.Column(db.Text, nullable=True)
    service_type = db.Column(db.String(80), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    approved_by_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    approval_date = db.Column(db.DateTime, nullable=True)
    documents = db.Column(db.JSON, nullable=True)  # Store document URLs/info
    average_rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    
    __mapper_args__ = {
        'polymorphic_identity': 'professional'
    }

# Customer table (inherits from User)
class Customer(User):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    customer_name = db.Column(db.String(80), nullable=False)  # Changed from 'name' to 'customer_name'
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    
    # Relationships
    service_requests = db.relationship('ServiceRequest', 
                                     backref='customer',
                                     lazy=True,
                                     cascade='all, delete-orphan')
    reviews = db.relationship('Reviews',
                            backref='customer',
                            lazy=True,
                            cascade='all, delete-orphan')
    
    __mapper_args__ = {
        'polymorphic_identity': 'customer'
    }

    def create_service_request(self, service_id, pin_code):
        service_request = ServiceRequest(
            customer_id=self.id,
            service_id=service_id,
            pin_code=pin_code,
            status='pending'
        )
        db.session.add(service_request)
        db.session.commit()
        return service_request
    
    def close_service_request(self, request_id):
        service_request = ServiceRequest.query.get(request_id)
        if service_request and service_request.customer_id == self.id:
            service_request.status = 'closed'
            service_request.closed_at = db.func.current_timestamp()
            db.session.commit()
            return True
        return False
    
    def add_review(self, service_request_id, rating, remarks):
        review = Reviews(
            service_request_id=service_request_id,
            customer_id=self.id,
            rating=rating,
            remarks=remarks
        )
        db.session.add(review)
        db.session.commit()
        return review

# Update ServiceRequest model to include more details
class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professional.id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'in_progress', 'completed', 'closed'
    pin_code = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    accepted_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    closed_at = db.Column(db.DateTime, nullable=True)
    special_instructions = db.Column(db.Text, nullable=True)
    final_amount = db.Column(db.Float, nullable=True)

# Update Reviews model to include customer relationship
class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

# Add a joining table for professionals and services
class ProfessionalServices(db.Model):
    __tablename__ = 'professional_services'
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professional.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)  # If this is the professional's primary service
    experience_years = db.Column(db.Integer, default=0)
    hourly_rate = db.Column(db.Float)  # Professional's custom rate for this service
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())
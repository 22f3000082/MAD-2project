from flask import current_app, Blueprint, request, jsonify, abort
from flask_security import Security, SQLAlchemyUserDatastore, hash_password,roles_required, current_user
from backend.application.models import db, User, Role, Admin, Customer, ServiceProfessional
from functools import wraps

import uuid

# Create Blueprint
auth = Blueprint('auth', __name__)

# Initialize Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

def init_security(app):
    security = Security(app, user_datastore)
    
    with app.app_context():
        # Create roles if they don't exist
        user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_datastore.find_or_create_role(name='professional', description='Service Professional')
        user_datastore.find_or_create_role(name='customer', description='Customer')
        
        db.session.commit()
        
        # Create default admin
        admin_email = 'admin@household.com'
        if not user_datastore.find_user(email=admin_email):
            # Create admin user
            admin = Admin(
                username='admin',
                email=admin_email,
                password=hash_password('admin123'),
                fs_uniquifier=str(uuid.uuid4()),
                active=True,
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            
            # Add admin role to user
            admin_user = user_datastore.find_user(email=admin_email)
            admin_role = user_datastore.find_role('admin')
            user_datastore.add_role_to_user(admin_user, admin_role)
            db.session.commit()

        # Create default customer
        customer_email = 'customer@household.com'
        if not user_datastore.find_user(email=customer_email):
            # Create customer user
            customer = Customer(
                username='customer',
                email=customer_email,
                password=hash_password('customer123'),
                fs_uniquifier=str(uuid.uuid4()),
                active=True,
                role='customer'
            )
            db.session.add(customer)
            
            # Add customer role to user
            customer_user = user_datastore.find_user(email=customer_email)
            customer_role = user_datastore.find_role('customer')
            user_datastore.add_role_to_user(customer_user, customer_role)
            db.session.commit()

# @auth.route('/register', methods=['POST'])
# def register():
#     try:
#         # data = request.get_json()
#         data = request.get_json(force=True, silent=True)
#         print("Received registration data:", data)  # Debug print
        
#         # Validate required fields
#         required_fields = ['email', 'password', 'role', 'username']
#         for field in required_fields:
#             if field not in data:
#                 return jsonify({'error': f'Missing required field: {field}'}), 400

#         # Check if user already exists
#         if User.query.filter_by(email=data['email']).first():
#             return jsonify({'error': 'Email already registered'}), 400

#         # Create base user
#         user = User(
#             email=data['email'],
#             password=hash_password(data['password']),
#             username=data['username'],  # Add username here
#             active=True,
#             fs_uniquifier=str(uuid.uuid4())
#         )

#         # Add role
#         role = Role.query.filter_by(name=data['role']).first()
#         if not role:
#             return jsonify({'error': f'Invalid role: {data["role"]}'}), 400
        
#         db.session.add(user)
#         user_datastore.add_role_to_user(user, role)
        
#         try:
#             # First commit to get the user ID
#             db.session.commit()
#         except Exception as e:
#             db.session.rollback()
#             print(f"Error creating user: {str(e)}")
#             return jsonify({'error': 'Error creating user'}), 500

#         # Create specific user type based on role
#         try:
#             if data['role'] == 'customer':
#                 if not all(field in data for field in ['phone', 'address', 'pin_code']):
#                     return jsonify({'error': 'Missing customer details'}), 400
                
#                 customer = Customer(
#                     user_id=user.id,
#                     address=data['address'],
#                     phone=data['phone'],
#                     pin_code=data['pin_code']
#                 )
#                 db.session.add(customer)
            
#             elif data['role'] == 'professional':
#                 if not all(field in data for field in ['service_type', 'experience']):
#                     return jsonify({'error': 'Missing professional details'}), 400
                
#                 professional = ServiceProfessional(
#                     user_id=user.id,
#                     service_type=data['service_type'],
#                     experience=int(data['experience']),
#                     description=data.get('description', ''),
#                     documents=data.get('documents', []),
#                     is_approved=False  # New professionals need approval
#                 )
#                 db.session.add(professional)

#             db.session.commit()
#             print(f"Successfully created {data['role']} profile")  # Debug print

#         except Exception as e:
#             db.session.rollback()
#             print(f"Error creating profile: {str(e)}")
#             # Delete the user if profile creation fails
#             try:
#                 User.query.filter_by(id=user.id).delete()
#                 db.session.commit()
#             except Exception as inner_e:
#                 print(f"Error cleaning up user: {str(inner_e)}")
#                 db.session.rollback()
#             return jsonify({'error': 'Error creating user profile', 'details': str(e)}), 500

#         return jsonify({
#             'message': 'User registered successfully',
#             'user': {
#                 'id': user.id,
#                 'email': user.email,
#                 'username': user.username,  # Include username in response
#                 'role': role.name,
#                 'is_approved': False if data['role'] == 'professional' else None
#             }
#         }), 201

#     except Exception as e:
#         print(f"Registration error: {str(e)}")
#         return jsonify({'error': 'Registration failed', 'details': str(e)}), 500

# Custom decorators for role-based access
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)  # Unauthorized
        if not current_user.has_role('admin'):
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

def professional_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.has_role('professional'):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
    
        if not current_user.has_role('customer'):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
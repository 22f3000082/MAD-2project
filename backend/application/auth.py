from flask import current_app, Blueprint, request, jsonify, abort
from flask_security import Security, SQLAlchemyUserDatastore, hash_password,roles_required, current_user
from backend.application.models import db, User, Role, Admin, Customer, ServiceProfessional, BlockedUsers, ServiceRequest, Reviews, Service
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
            customer_user = User(
                username='customer',
                email=customer_email,
                password=hash_password('customer123'),
                fs_uniquifier=str(uuid.uuid4()),
                active=True
            )
            db.session.add(customer_user)
            db.session.commit()
            
            # Add customer role to user
            customer_role = user_datastore.find_role('customer')
            user_datastore.add_role_to_user(customer_user, customer_role)
            
            # Create customer profile with required fields
            customer = Customer(
                # user_id=customer_user.id,
                customer_name='Default Customer',  # Add the required customer_name
                phone='1234567890',                # Add default phone
                address='123 Default Street',      # Add default address
                pin_code='12345'                   # Add default pin_code
            )
            db.session.add(customer)
            db.session.commit()

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check required fields
        if 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find the user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check password
        from flask_security.utils import verify_password
        if not verify_password(data['password'], user.password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check if user is active
        if not user.active:
            return jsonify({'error': 'Account is inactive'}), 403
        
        # Check if user is blocked
        if user.is_blocked:
            return jsonify({'error': 'Account has been blocked. Please contact support.'}), 403
        
        # Check if professional is approved before allowing login
        if user.role == 'professional':
            professional = ServiceProfessional.query.filter_by(id=user.id).first()
            if professional:
                # Allow login even if not approved
                if not professional.is_approved:
                    # Instead of blocking login, just return a warning
                    login_user(user)
                    print(f"Professional login success for non-approved user: {user.email}")
                    
                    token = user.get_auth_token()
                    print(f"Generated token: {token[:10]}...")  # Only print first 10 chars for security
                    
                    response = jsonify({
                        'token': token,
                        'user': {
                            'id': user.id,
                            'email': user.email,
                            'username': user.username,
                            'role': user.role,
                            'is_approved': False,
                            'warning': 'Your account is pending approval. Some features may be restricted.'
                        }
                    })
                    return response, 200
            else:
                # Professional record not found
                print(f"Professional record not found for user {user.id}")
                return jsonify({'error': 'Professional profile not found'}), 403
        
        # Log in the user
        from flask_security import login_user
        login_user(user)
        
        # Generate token
        token = user.get_auth_token()
        print(f"Login successful for user: {user.id} with role: {user.role}")
        print(f"Generated token: {token[:10]}...")  # Only print first 10 chars for security
        
        # Create response with token and user data
        response = jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.role,
                'is_approved': ServiceProfessional.query.get(user.id).is_approved if user.role == 'professional' else None
            }
        })
        
        return response, 200
    
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed', 'details': str(e)}), 500

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
from flask import Blueprint, jsonify, request,render_template, url_for, make_response
from backend.application.models import db, User, ServiceProfessional, Service, Customer
from backend.application.auth import admin_required, user_datastore, init_security
from flask_security import auth_required, login_required, hash_password, roles_required, login_user, current_user
from flask_security.utils import verify_password
import uuid
# from app import create_app as app
# from app import create_app

# app = create_app()  # Now, app is a Flask instance
# Create main blueprint for general routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

admin = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin.route('/', methods=['GET'])
@auth_required('token')
@admin_required
def admin_home():
    return "Welcome to the admin dashboard!"

@admin.route('/api/admin/users', methods=['GET'])
@auth_required('token')    # we have token based auth
@admin_required
def get_all_users():
    users = User.query.filter(User.role.in_(['professional', 'customer'])).all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'is_blocked': user.is_blocked,
        'date_created': user.date_created.isoformat(),
        'last_login': user.last_login_at.isoformat() if user.last_login_at else None,
        'name': user.name if hasattr(user, 'name') else None,
        'is_approved': user.is_approved if isinstance(user, ServiceProfessional) else None
    } for user in users])

@admin.route('/api/admin/professionals/<int:prof_id>/approve', methods=['POST'])
@auth_required('token')
@admin_required
def approve_professional(prof_id):
    professional = ServiceProfessional.query.get_or_404(prof_id)
    professional.is_approved = True
    db.session.commit()
    return jsonify({'message': 'Professional approved successfully'})

@admin.route('/api/admin/users/<int:user_id>/toggle-block', methods=['POST'])
@auth_required('token')
@admin_required
def toggle_block_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_blocked = not user.is_blocked
    db.session.commit()
    return jsonify({
        'message': f'User {"blocked" if user.is_blocked else "unblocked"} successfully'
    })

# @admin.route('/api/admin/services', methods=['GET', 'POST'])
# @auth_required('token')
# @admin_required
# def manage_services():
#     if request.method == 'GET':
#         services = Service.query.all()
#         return jsonify([{
#             'id': service.id,
#             'name': service.name,
#             'base_price': service.base_price,
#             'created_by_admin_id': service.created_by_admin_id
#         } for service in services])
    
# try:
#     data = request.get_json()
# except:
#     return jsonify({'error': 'No data provided'}), 400
        
#         # Validate required fields
#         required_fields = ['name', 'base_price', 'time_required', 'category']
#         for field in required_fields:
#             if field not in data:
#                 return jsonify({'error': f'{field} is required'}), 400
        
#         # Create new service with all required fields
#         new_service = Service(
#         name=data['name'],
#         base_price=data['base_price'],
#         time_required=data['time_required'],
#             category=data['category'],
#             created_by_admin_id=current_user.id,  # Use current admin's ID instead of sending it
#             description=data.get('description'),  # Optional fields
#             is_active=data.get('is_active', True),
#             availability=data.get('availability', 'available'),
#             min_booking_hours=data.get('min_booking_hours', 1),
#             max_booking_hours=data.get('max_booking_hours', 8),
#             cancellation_policy=data.get('cancellation_policy')
#         )
        
#     db.session.add(new_service)
#     db.session.commit()
#     return jsonify({'message': 'Service created successfully', 'id': new_service.id}), 201
#     except Exception as e:
#         db.session.rollback()
#         print(f"Error creating service: {str(e)}")
#         return jsonify({'error': f'Failed to create service: {str(e)}'}), 500

# @admin.route('/api/admin/services/<int:service_id>', methods=['PUT', 'DELETE'])
# @auth_required('token')
# @admin_required
# def service_operations(service_id):
#     service = Service.query.get_or_404(service_id)
    
#     if request.method == 'DELETE':
#         db.session.delete(service)
#         db.session.commit()
#         return jsonify({'message': 'Service deleted successfully'})
    
#     data = request.get_json()
#     service.name = data.get('name', service.name)
#     service.base_price = data.get('base_price', service.base_price)
#     db.session.commit()
#     return jsonify({'message': 'Service updated successfully'})


@admin.route('/api/admin/services', methods=['GET', 'POST'])
@auth_required('token')
@admin_required
def manage_services():
    if request.method == 'GET':
        services = Service.query.all()
        return jsonify([{
            'id': service.id,
            'name': service.name,
            'base_price': service.base_price,
            'created_by_admin_id': service.created_by_admin_id
        } for service in services])
    
    data = request.get_json()
    new_service = Service(
        name=data['name'],
        base_price=data['base_price'],
        created_by_admin_id=data['admin_id']
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify({'message': 'Service created successfully', 'id': new_service.id})
    
# Create a new blueprint for authentication
auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return make_response('', 200)
        
    try:
        data = request.form
#         data = request.get_json(force=True, silent=True)

        print("Received registration data:", data)
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'role']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create base user
        user_data = {
            'name': data['name'],
            'email': data['email'],
            'password': hash_password(data['password']),
            'role': data['role'],
            'fs_uniquifier': str(uuid.uuid4())
        }
        
        if data['role'] == 'customer':
            # Validate customer fields
            if not all([data.get('phone'), data.get('address'), data.get('pin_code')]):
                return jsonify({'error': 'Phone, address and PIN code are required for customers'}), 400
                
            user = Customer(
                **user_data,
                phone=data['phone'],
                address=data['address'],
                pin_code=data['pin_code']
            )
        elif data['role'] == 'professional':
            # Validate professional fields
            if not all([data.get('service_type'), data.get('experience')]):
                return jsonify({'error': 'Service type and experience are required for professionals'}), 400
                
            user = ServiceProfessional(
                **user_data,
professional_name=data['name'],  # Set professional_name field instead of name
                service_type=data['service_type'],
                experience=data['experience'],
                description=data.get('description', ''),
                is_approved=False
            )
            
            # Handle document uploads if any
            if 'documents' in request.files:
                documents = request.files.getlist('documents')
                # Process documents here
        else:
            return jsonify({'error': 'Invalid role'}), 400
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Registration successful',
            'user_id': user.id
        }), 201
        
    except Exception as e:
        print(f"Registration error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@roles_required('admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No data provided'}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400
        
        # Try to find the user in each type of user table
        user = None
        
        # Check Customer table
        customer = Customer.query.filter_by(email=email).first()
        if customer:
            user = customer
            user_type = 'customer'
        else:
            # Check Professional table
            professional = ServiceProfessional.query.filter_by(email=email).first()
            if professional:
                user = professional
                user_type = 'professional'
            else:
                # Check Admin table (regular User)
                admin = User.query.filter_by(email=email, role='admin').first()
                if admin:
                    user = admin
                    user_type = 'admin'
        
        if not user:
            return jsonify({'message': 'Invalid email or password'}), 401
            
        if not user.is_active:
            return jsonify({'message': 'Account is blocked. Please contact admin.'}), 403
            
        if user_type == 'professional' and not user.is_approved:
            return jsonify({'message': 'Your account is pending approval'}), 403
            
        if verify_password(password, user.password):
            login_user(user)
            token = user.get_auth_token()   #generate a login token
            
            # Get user details based on type
            user_data = {
                'id': user.id,
                'email': user.email,
                'role': user_type
            }
            
            # Add name based on user type
            if user_type == 'customer':
                user_data['name'] = user.customer_name
            elif user_type == 'professional':
                user_data['name'] = user.professional_name
            else:
                user_data['name'] = 'Admin'
                
            response = jsonify({
                'message': 'Logged in successfully',
                'token': token,
                'user': user_data
            })
            
            # Set session cookie
            response.set_cookie(
                'session',
                token,
                httponly=True,          #prevents client side js from accessing the cookie
                secure=True,            #only send the cookie over https
                samesite='Strict',      #prevents the cookie from being sent along with requests to other sites
                max_age=86400  # 24 hours
            )
            
            return response
            
        return jsonify({'message': 'Invalid email or password'}), 401
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'message': 'An error occurred during login'}), 500 

# Create API blueprint
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/services', methods=['GET'])
def get_services():
    try:
        services = Service.query.all()
        return jsonify([{
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'base_price': service.base_price,
            'category': service.category
        } for service in services]), 200
    except Exception as e:
        print(f"Error fetching services: {str(e)}")
        return jsonify({'error': 'Failed to fetch services'}), 500

@api.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Server is running'
    })

@api.route('/service-types', methods=['GET', 'OPTIONS'])
def get_service_types():
    if request.method == 'OPTIONS':
        return make_response('', 200)
        
    try:
        service_types = [
            'AC Repair',
            'Plumbing',
            'Electrical',
            'Carpentry',
            'Painting',
            'Cleaning',
            'Pest Control',
            'Appliance Repair',
            'Moving Services',
            'Gardening'
        ]
        return jsonify(service_types)
    except Exception as e:
        print(f"Error in get_service_types: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Register blueprints
def init_app(app):
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(api)
    return app 
from wsgiref import headers
from flask import Blueprint, jsonify, request,render_template, url_for, make_response
from backend.application.models import db, User, ServiceProfessional, Service, Customer
from backend.application.auth import admin_required, user_datastore, init_security
from flask_security import auth_required, login_required, hash_password, roles_required, login_user, current_user
from flask_security.utils import verify_password
import uuid
from datetime import datetime
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

# @admin.route('/users', methods=['GET'])
# def handle_users_options_and_get():
#     if request.method == 'OPTIONS':
#         response = make_response()
#         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8081')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authentication-Token')
#         response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
#         response.headers.add('Access-Control-Allow-Credentials', 'true')
#         return response
        
#     # The GET part requires authentication
#     return get_all_users()

@admin.route('/users', methods=['GET'])
@auth_required('token')
@admin_required
def get_all_users():
    try:
        # Debugging - print all headers to see what's coming in
        print("Request headers:", dict(request.headers))
        auth_token = request.headers.get('Authentication-Token')
        print(f"Auth token received: {auth_token[:10] if auth_token else 'None'}")
        
        # Log authentication info for debugging
        auth_token = request.headers.get('Authentication-Token')
        print(f"Received token for /api/admin/users: {auth_token[:10]}..." if auth_token else "No token received")
        print(f"Current user: {current_user}")

        users = User.query.filter(User.role.in_(['professional', 'customer'])).all()
        result = []
        
        for user in users:
            # Create base user data that always exists
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_blocked': user.is_blocked,
                'date_created': user.date_created.isoformat() if user.date_created else None,
                'last_login': user.last_login_at.isoformat() if user.last_login_at else None,
                'name': None  # Default value
            }
            
            # Add role-specific fields
            if user.role == 'professional':
                professional = ServiceProfessional.query.get(user.id)
                if professional:
                    user_data.update({
                        'name': professional.professional_name,
                        'is_approved': professional.is_approved,
                        'service_type': professional.service_type,
                        'experience': professional.experience
                    })
            elif user.role == 'customer':
                customer = Customer.query.get(user.id)
                if customer:
                    user_data.update({
                        'name': customer.customer_name,
                        'phone': customer.phone,
                        'address': customer.address
                    })
            
            # If name is still None, use username as fallback
            if user_data['name'] is None:
                user_data['name'] = user_data['username']
                
            result.append(user_data)
        
        print(f"Returning {len(result)} users")
        return jsonify(result)
        
    except Exception as e:
        print(f"Error fetching users: {str(e)}")
        return jsonify({'error': 'Failed to fetch users'}), 500

@admin.route('/professionals/<int:prof_id>/approve', methods=['POST'])
@auth_required('token')
@admin_required
def approve_professional(prof_id):
    try:
        professional = ServiceProfessional.query.get_or_404(prof_id)
        if professional.is_approved:
            return jsonify({'message': 'Professional already approved'}), 400
            
        professional.is_approved = True
        professional.approved_by_id = current_user.id
        professional.approval_date = db.func.current_timestamp()
        db.session.commit()
        
        return jsonify({'message': 'Professional approved successfully'})
    except Exception as e:
        db.session.rollback()
        print(f"Error approving professional: {str(e)}")
        return jsonify({'error': f'Failed to approve professional: {str(e)}'}), 500

@admin.route('/users/<int:user_id>/block', methods=['POST'])
@auth_required('token')
@admin_required
def block_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        if user.is_blocked:
            return jsonify({'message': 'User already blocked'}), 400
            
        data = request.get_json()
        reason = data.get('reason', 'No reason provided')
        
        # Create block record
        blocked_record = BlockedUsers(
            user_id=user_id,
            admin_id=current_user.id,
            block_reason=reason,
            blocked_at=db.func.current_timestamp()
        )
        
        user.is_blocked = True
        db.session.add(blocked_record)
        db.session.commit()
        
        return jsonify({'message': 'User blocked successfully'})
    except Exception as e:
        db.session.rollback()
        print(f"Error blocking user: {str(e)}")
        return jsonify({'error': f'Failed to block user: {str(e)}'}), 500

@admin.route('/users/<int:user_id>/unblock', methods=['POST'])
@auth_required('token')
@admin_required
def unblock_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        if not user.is_blocked:
            return jsonify({'message': 'User is not blocked'}), 400
            
        # Update the latest block record
        block_record = BlockedUsers.query.filter_by(
            user_id=user_id,
            unblocked_at=None
        ).order_by(BlockedUsers.blocked_at.desc()).first()
        
        if block_record:
            block_record.unblocked_at = db.func.current_timestamp()
            
        user.is_blocked = False
        db.session.commit()
        
        return jsonify({'message': 'User unblocked successfully'})
    except Exception as e:
        db.session.rollback()
        print(f"Error unblocking user: {str(e)}")
        return jsonify({'error': f'Failed to unblock user: {str(e)}'}), 500

# @admin.route('/api/admin/professionals/<int:prof_id>/approve', methods=['POST'])
# @auth_required('token')
# @admin_required
# def approve_professional(prof_id):
#     professional = ServiceProfessional.query.get_or_404(prof_id)
#     professional.is_approved = True
#     db.session.commit()
#     return jsonify({'message': 'Professional approved successfully'})

# @admin.route('/api/admin/users/<int:user_id>/toggle-block', methods=['POST'])
# @auth_required('token')
# @admin_required
# def toggle_block_user(user_id):
#     token = request.headers.get('Authentication-Token')
#     print(f'Received Token: {token}')
#     user = User.query.get_or_404(user_id)
#     user.is_blocked = not user.is_blocked
#     db.session.commit()
#     return jsonify({
#         'message': f'User {"blocked" if user.is_blocked else "unblocked"} successfully'
#     })

@admin.route('/services', methods=['GET', 'POST'])
@auth_required('token')
@admin_required
def admin_services():
    try:
        # if request.method == 'OPTIONS':
        #     response = make_response()
        #     response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8082')
        #     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authentication-Token')
        #     response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        #     response.headers.add('Access-Control-Allow-Credentials', 'true')
        #     return response

        # token = request.headers.get('Authentication-Token')
        # if not token:
        #     return jsonify({'error': 'No authentication token provided'}), 401

        if request.method == 'GET':
            services = Service.query.all()
            result = []
            for service in services:
                result.append({
                    'id': service.id,
                    'name': service.name,
                    'description': service.description,
                    'base_price': service.base_price,
                    'time_required': service.time_required,
                    'category': service.category,
                    'is_active': service.is_active
                })
            response = jsonify(result)
        elif request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400

            required_fields = ['name', 'description', 'base_price', 'time_required']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400

            new_service = Service(
                name=data['name'],
                description=data['description'],
                base_price=data['base_price'],
                time_required=data['time_required'],
                category=data.get('category', 'General'),
                is_active=True
            )
            db.session.add(new_service)
            db.session.commit()
            
            response = jsonify({
                'id': new_service.id,
                'name': new_service.name,
                'description': new_service.description,
                'base_price': new_service.base_price,
                'time_required': new_service.time_required,
                'category': new_service.category,
                'is_active': new_service.is_active
            })

        # Add CORS headers to response
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authentication-Token')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    except Exception as e:
        print(f"Error in admin_services: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@admin.route('/services/<int:service_id>', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
@auth_required('token')
@admin_required
def admin_service(service_id):
    try:
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8081')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authentication-Token')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,DELETE,OPTIONS')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response

        service = Service.query.get_or_404(service_id)
        
        if request.method == 'GET':
            response = jsonify({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'base_price': service.base_price,
                'time_required': service.time_required,
                'category': service.category,
                'is_active': service.is_active
            })
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400

            if 'name' in data:
                service.name = data['name']
            if 'description' in data:
                service.description = data['description']
            if 'base_price' in data:
                service.base_price = data['base_price']
            if 'time_required' in data:
                service.time_required = data['time_required']
            if 'category' in data:
                service.category = data['category']
            if 'is_active' in data:
                service.is_active = data['is_active']

            db.session.commit()
            response = jsonify({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'base_price': service.base_price,
                'time_required': service.time_required,
                'category': service.category,
                'is_active': service.is_active
            })
        elif request.method == 'DELETE':
            db.session.delete(service)
            db.session.commit()
            response = jsonify({'message': 'Service deleted successfully'})

        # Add CORS headers to response
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8081')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authentication-Token')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    except Exception as e:
        print(f"Error in admin_service: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# # Add CORS headers to all responses
# @admin.after_request
# def add_cors_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8081'
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authentication-Token'
#     response.headers['Access-Control-Allow-Credentials'] = 'true'
#     return response

# # Handle OPTIONS requests
# @admin.route('/users', methods=['OPTIONS'])
# def handle_users_options():
#     response = make_response()
#     response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8081')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authentication-Token')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
#     response.headers.add('Access-Control-Allow-Credentials', 'true')
#     return response

# Create a new blueprint for authentication
auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return make_response('', 200)
        
    try:
        data = request.form
        print("Received registration data:", data)
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'role', 'username']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already taken'}), 400
        
        # Create base user data - exclude 'name' as it's not a field in User model
        user_data = {
            'username': data['username'],
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
                customer_name=data['name'],  # Map 'name' from form to 'customer_name'
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
                professional_name=data['name'],  # Map 'name' from form to 'professional_name'
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
# Remove the auth_required decorator from login function - users can't authenticate before logging in
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
        # user = None
        user = User.query.filter_by(email=data.get('email')).first()
        
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
            
            # Add diagnostic logging
            print(f"Login successful for user: {user.id} with role: {user_type}")
            print(f"Generated token: {token[:10]}...")
            
            # Get user details based on type
            user_data = {
                'id': user.id,
                'email': user.email,
                'username': user.username,  # Add username to response
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
                # During development, secure should be False for localhost testing
                secure=False,
                samesite='Lax',  # Use 'Lax' instead of 'Strict' for development
                max_age=86400  # 24 hours
            )
            
            return response
            
        return jsonify({'message': 'Invalid email or password'}), 401
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'message': 'An error occurred during login'}), 500 

# Create API blueprint
api = Blueprint('api', __name__, url_prefix='/api')

# @api.route('/services', methods=['GET'])
# def get_services():
#     try:
#         services = Service.query.all()
#         return jsonify([{
#             'id': service.id,
#             'name': service.name,
#             'description': service.description,
#             'base_price': service.base_price,
#             'category': service.category
#         } for service in services]), 200
#     except Exception as e:
#         print(f"Error fetching services: {str(e)}")
#         return jsonify({'error': 'Failed to fetch services'}), 500

@api.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Server is running'
    })

@api.route('/service-types', methods=['GET', 'OPTIONS'])
def get_service_types():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authentication-Token,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,OPTIONS')
        return response
        
    try:
        # Hardcoded list of service types
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
        response = jsonify(service_types)
        # Add CORS headers to make it accessible from the frontend
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print(f"Error in get_service_types: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Add these professional endpoints to the existing API blueprint
@api.route('/professional/assignments', methods=['GET'])
@auth_required('token')
def get_professional_assignments():
    try:
        # Ensure the current user is a professional
        if current_user.role != 'professional':
            return jsonify({'error': 'Unauthorized access'}), 403
            
        # Get status filter if provided
        status = request.args.get('status')
        
        # Base query to get service requests assigned to this professional
        query = ServiceRequest.query.filter_by(professional_id=current_user.id)
        
        # Apply status filter if provided
        if status:
            query = query.filter_by(status=status)
            
        # Get all matching requests with related data
        service_requests = query.all()
        
        # Prepare response data
        result = []
        for req in service_requests:
            # Get service details
            service = Service.query.get(req.service_id)
            # Get customer details
            customer = Customer.query.get(req.customer_id)
            # Get review if any
            review = Reviews.query.filter_by(service_request_id=req.id).first()
            
            request_data = {
                'id': req.id,
                'status': req.status,
                'pin_code': req.pin_code,
                'created_at': req.created_at.isoformat() if req.created_at else None,
                'accepted_at': req.accepted_at.isoformat() if req.accepted_at else None,
                'completed_at': req.completed_at.isoformat() if req.completed_at else None,
                'closed_at': req.closed_at.isoformat() if req.closed_at else None,
                'special_instructions': req.special_instructions,
                'final_amount': req.final_amount,
                'service': {
                    'id': service.id,
                    'name': service.name,
                    'base_price': service.base_price,
                    'description': service.description
                },
                'customer': {
                    'id': customer.id,
                    'customer_name': customer.customer_name,
                    'phone': customer.phone,
                    'address': customer.address
                }
            }
            
            # Add review data if available
            if review:
                request_data['review'] = {
                    'id': review.id,
                    'rating': review.rating,
                    'remarks': review.remarks,
                    'date_created': review.date_created.isoformat()
                }
                
            result.append(request_data)
            
        return jsonify(result)
    except Exception as e:
        print(f"Error fetching assignments: {str(e)}")
        return jsonify({'error': 'Failed to fetch assignments'}), 500

@api.route('/professional/requests/<int:request_id>', methods=['PUT'])
@auth_required('token')
def update_request_status(request_id):
    try:
        # Ensure the current user is a professional
        if current_user.role != 'professional':
            return jsonify({'error': 'Unauthorized access'}), 403
            
        # Get the service request
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        # Ensure the request is assigned to this professional
        if service_request.professional_id != current_user.id and service_request.professional_id is not None:
            return jsonify({'error': 'This request is not assigned to you'}), 403
            
        # Get the new status from request data
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'error': 'No status provided'}), 400
            
        # Validate status transition
        valid_transitions = {
            'pending': ['in_progress', 'rejected'],
            'in_progress': ['completed'],
            'completed': []  # Can't change from completed
        }
        
        if service_request.status not in valid_transitions or new_status not in valid_transitions.get(service_request.status, []):
            return jsonify({'error': f'Cannot transition from {service_request.status} to {new_status}'}), 400
            
        # Update the request status
        service_request.status = new_status
        
        # If accepting request, assign this professional
        if new_status == 'in_progress' and service_request.professional_id is None:
            service_request.professional_id = current_user.id
            
        # Set timestamps based on status
        if new_status == 'in_progress':
            service_request.accepted_at = db.func.current_timestamp()
        elif new_status == 'completed':
            service_request.completed_at = db.func.current_timestamp()
            
        db.session.commit()
        
        return jsonify({
            'message': 'Service request updated successfully',
            'id': service_request.id,
            'status': service_request.status
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error updating request status: {str(e)}")
        return jsonify({'error': 'Failed to update request status'}), 500

@api.route('/professional/profile', methods=['GET'])
@auth_required('token')
def get_professional_profile():
    try:
        # Ensure the current user is a professional
        if current_user.role != 'professional':
            return jsonify({'error': 'Unauthorized access'}), 403
            
        # Get the professional's profile
        professional = ServiceProfessional.query.get(current_user.id)
        
        if not professional:
            return jsonify({'error': 'Professional profile not found'}), 404
            
        # Prepare response data
        result = {
            'id': professional.id,
            'professional_name': professional.professional_name,
            'service_type': professional.service_type,
            'description': professional.description,
            'experience': professional.experience,
            'is_approved': professional.is_approved,
            'approval_date': professional.approval_date.isoformat() if professional.approval_date else None,
            'average_rating': professional.average_rating,
            'total_reviews': professional.total_reviews
        }
        
        return jsonify(result)
    except Exception as e:
        print(f"Error fetching professional profile: {str(e)}")
        return jsonify({'error': 'Failed to fetch profile'}), 500

# Register blueprints
def init_app(app):
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(api)
    return app
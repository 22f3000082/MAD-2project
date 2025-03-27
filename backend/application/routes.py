from wsgiref import headers
from flask import Blueprint, jsonify, request,render_template, url_for, make_response, send_from_directory
from backend.application.models import db, User, ServiceProfessional, Service, Customer, Admin, BlockedUsers, ServiceRequest, Reviews
from backend.application.auth import admin_required, user_datastore, init_security
from flask_security import auth_required, login_required, hash_password, roles_required, login_user, current_user
from flask_security.utils import verify_password
import uuid
from datetime import datetime
from celery.result import AsyncResult
import os
from .task import download_csv_report, monthly_report
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

@admin.route('/users', methods=['GET'])
@auth_required('token')
@admin_required
def get_all_users():
    try:
        # Debugging - print all headers to see what's coming in
        # print("Request headers:", dict(request.headers))
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

@admin.route('/services', methods=['GET', 'POST'])
@auth_required('token')
@admin_required
def admin_services():
    try:
        if request.method == 'GET':
            services = Service.query.all()
            result = []
            for service in services:
                # Format service data to match frontend expectations
                result.append({
                    'id': service.id,
                    'name': service.name,
                    'description': service.description,
                    'base_price': service.base_price,  # Changed to camelCase
                    'timeRequired': service.time_required,  # Changed to camelCase
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

            # Enhanced debugging
            print(f"Creating service with data: {data}")
            print(f"Current user: ID={current_user.id}, Role={current_user.role}")
            
            # Make sure we have an admin record
            admin_record = Admin.query.get(current_user.id)
            if not admin_record:
                print(f"Creating new admin record for user {current_user.id}")
                # Create an Admin record linked to the current user
                admin_record = Admin(id=current_user.id)
                db.session.add(admin_record)
                db.session.flush()  # Get ID without committing
                print(f"Created admin record with ID: {admin_record.id}")
            else:
                print(f"Found existing admin record: {admin_record.id}")

            try:
                new_service = Service(
                    name=data['name'],
                    description=data['description'],
                    base_price=float(data['base_price']),
                    time_required=int(data['time_required']),
                    category=data.get('category', 'General'),
                    is_active=True,
                    created_by_admin_id=admin_record.id  # Use admin_record.id instead
                )
                
                db.session.add(new_service)
                db.session.commit()
                print(f"Service successfully created with ID: {new_service.id}")
                
                response = jsonify({
                    'id': new_service.id,
                    'name': new_service.name,
                    'description': new_service.description,
                    'base_price': new_service.base_price,
                    'time_required': new_service.time_required,
                    'category': new_service.category,
                    'is_active': new_service.is_active
                })
            except Exception as inner_error:
                db.session.rollback()
                print(f"Error creating service: {str(inner_error)}")
                # Get detailed error information
                import traceback
                traceback.print_exc()
                return jsonify({'error': f'Failed to create service: {str(inner_error)}'}), 500

        # Ensure#  consistent CORS headers
        
        return response

    except Exception as e:
        print(f"Error in admin_services: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

@admin.route('/services/<int:service_id>', methods=['GET', 'PUT'])
@auth_required('token')
@admin_required
def update_service(service_id):
    try:
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
            return response  # Added return statement here
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
            return response
        else:
            return jsonify({'error': 'Method not allowed'}), 405

    except Exception as e:
        print(f"Error in admin_service: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@admin.route('/services/<int:service_id>', methods=['DELETE'])
@auth_required('token')
@admin_required
def delete_service(service_id):
    try:
        print(f"Attempting to delete service {service_id}")
        service = Service.query.get_or_404(service_id)
        
        # Check for existing requests
        existing_requests = ServiceRequest.query.filter_by(service_id=service_id).first()
        
        if existing_requests:
            # Mark as inactive instead of deleting
            service.is_active = False
            db.session.commit()
            return jsonify({
                'message': f'Service {service_id} marked as inactive (has existing requests)',
                'status': 'deactivated'
            })
        
        # No existing requests - safe to delete
        db.session.delete(service)
        db.session.commit()
        
        print(f"Service {service_id} deleted successfully")
        return jsonify({
            'message': f'Service {service_id} deleted successfully',
            'status': 'deleted'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting service {service_id}: {str(e)}")
        return jsonify({
            'error': 'Failed to delete service',
            'message': str(e)
        }), 500

@admin.route('/requests', methods=['GET'])
@auth_required('token')
@admin_required
def get_service_requests():
    try:
        # Get all service requests with optional status filter
        status = request.args.get('status')
        
        # Base query
        query = ServiceRequest.query
        
        # Apply status filter if provided
        if status:
            query = query.filter_by(status=status)
            
        # Get all matching requests
        service_requests = query.all()
        
        # Prepare response data
        result = []
        for req in service_requests:
            # Get service details
            service = Service.query.get(req.service_id)
            # Get customer details
            customer = Customer.query.get(req.customer_id)
            # Get professional details if assigned
            professional = None
            if req.professional_id:
                professional = ServiceProfessional.query.get(req.professional_id)
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
                } if service else None,
                'customer': {
                    'id': customer.id,
                    'customer_name': customer.customer_name,
                    'phone': customer.phone,
                    'address': customer.address
                } if customer else None,
                'professional': {
                    'id': professional.id,
                    'professional_name': professional.professional_name,
                    'service_type': professional.service_type,
                    'experience': professional.experience
                } if professional else None
            }
            
            # Add review data if available
            if review:
                request_data['review'] = {
                    'id': review.id,
                    'rating': review.rating,
                    'remarks': review.remarks,
                    'date_created': review.date_created.isoformat() if review.date_created else None
                }
                
            result.append(request_data)
            
        return jsonify(result)
    except Exception as e:
        print(f"Error fetching service requests: {str(e)}")
        return jsonify({'error': 'Failed to fetch service requests'}), 500

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
        
        # Create base user data 
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
                max_age=3000 
            )
            
            return response
            
        return jsonify({'message': 'Invalid email or password'}), 401
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'message': 'An error occurred during login'}), 500 


@auth.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'message': 'Logged out successfully'})
    response.set_cookie('session', '', expires=0)  # Clears the session cookie
    return response

# Create API blueprint
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/export')
def export_csv():
    try:
        print("Starting CSV export...")
        # Check if the static directory exists and is writable
        import os
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        static_dir = os.path.join(PROJECT_ROOT, 'static')
        os.makedirs(static_dir, exist_ok=True)
        # static_dir = os.path.join(os.path.dirname(__file__), 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
            print(f"Created static directory: {static_dir}")
        
        # Launch the celery task
        result = download_csv_report.delay()
        print(f"CSV export task launched with ID: {result.id}")
        return jsonify({
            'id': result.id,
            'message': 'Report generation started'
        })
    except Exception as e:
        import traceback
        print(f"Error starting CSV export: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': f'Failed to start report generation: {str(e)}'
        }), 500

@api.route('/csv_result/<task_id>')
def csv_result(task_id):
    try:
        print(f"Checking CSV result for task ID: {task_id}")
        res = AsyncResult(task_id)

        if not res.ready():
            return jsonify({'ready': False, 'message': 'Report still generating...'}), 202
        
        if not res.successful():
            return jsonify({'ready': True, 'successful': False, 'error': 'Report generation failed'}), 500

        filename = res.result
        if filename.startswith("ERROR:"):
            return jsonify({'ready': True, 'successful': False, 'error': filename[6:]}), 500

        # Validate file existence
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        static_dir = os.path.join(PROJECT_ROOT, 'static')
        # static_dir = os.path.join(os.path.dirname(__file__), 'static')
        file_path = os.path.join(static_dir, filename)
        print(f"Flask looking for file at: {file_path}")
        if not os.path.exists(file_path):
            return jsonify({'ready': True, 'successful': False, 'error': 'File not found'}), 500
        
        print(f"Looking for file at: {file_path}")

        return send_from_directory('/mnt/c/Users/91829/OneDrive/Documents/VS CODE/Household_service_22f3000082/static', filename, as_attachment=True, download_name=filename)

    except Exception as e:
        return jsonify({'error': f'Error retrieving report: {str(e)}'}), 500
# app = Flask(__name__, static_folder='static')

@api.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@api.route('/mail')
def send_mail():
    res= monthly_report.delay()
    return{
    #    "task_id" : task_id,
       "status" :"Task started"
    }


@api.route('/health', methods=['GET'])
def health_check():
    try:
        # Check database connectivity
        db_status = True
        try:
            db.session.execute('SELECT 1')
        except Exception as e:
            db_status = False
            print(f"Database connection error in health check: {str(e)}")
            
        return jsonify({
            'status': 'healthy' if db_status else 'degraded',
            'database': 'connected' if db_status else 'disconnected',
            'message': 'Server is running',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Health check error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@api.route('/service-types', methods=['GET'])
def get_service_types():
    try:
        # Define default categories that should always be available
        default_categories = [
            'AC Repair', 'Plumbing', 'Electrical', 'Carpentry', 'Painting',
            'Cleaning', 'Pest Control', 'Appliance Repair', 'Moving Services', 'Gardening'
        ]
        
        # Log the defaults for debugging
        print(f"Default categories: {default_categories}")
        
        # Query the database for unique categories from the Service table
        categories = db.session.query(Service.category).distinct().all()
        
        # Extract the category strings from the result tuples
        db_categories = [category[0] for category in categories if category[0]]
        print(f"Categories from database: {db_categories}")
        
        # Merge database categories with default categories (no duplicates)
        service_types = list(set(db_categories + default_categories))
        
        # Sort alphabetically for consistent display
        service_types.sort()
        
        print(f"Returning {len(service_types)} service types: {service_types}")
        return jsonify(service_types)
    except Exception as e:
        print(f"Error in get_service_types: {str(e)}")
        return jsonify({
            'error': 'Internal server error', 
            'details': str(e),
            'fallback_categories': [
                'AC Repair', 'Plumbing', 'Electrical', 'Carpentry', 'Painting',
                'Cleaning', 'Pest Control', 'Appliance Repair', 'Moving Services', 'Gardening'
            ]
        }), 500

# Add a debug endpoint to inspect service categories
@api.route('/debug/service-types', methods=['GET'])
def debug_service_types():
    """Debug endpoint to view all service categories in the system"""
    try:
        # Get all services
        services = Service.query.all()
        
        # Get distinct categories from database
        db_categories = db.session.query(Service.category).distinct().all()
        db_categories = [category[0] for category in categories if category[0]]
        
        # Default categories
        default_categories = [
            'AC Repair', 'Plumbing', 'Electrical', 'Carpentry', 'Painting',
            'Cleaning', 'Pest Control', 'Appliance Repair', 'Moving Services', 'Gardening'
        ]
        
        return jsonify({
            'total_services': len(services),
            'unique_categories_in_db': db_categories,
            'default_categories': default_categories,
            'all_services': [
                {
                    'id': service.id,
                    'name': service.name,
                    'category': service.category,
                    'is_active': service.is_active
                }
                for service in services
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@api.route('/professional/reviews', methods=['GET'])
@auth_required('token')
def get_professional_reviews():
    try:
        # Ensure the current user is a professional
        if current_user.role != 'professional':
            return jsonify({'error': 'Unauthorized access'}), 403
            
        # Get all reviews for this professional
        review_data = []
        service_requests = ServiceRequest.query.filter_by(professional_id=current_user.id).all()
        
        for req in service_requests:
            review = Reviews.query.filter_by(service_request_id=req.id).first()
            if review:
                # Get customer name
                customer = Customer.query.get(review.customer_id)
                # Get service name
                service = Service.query.get(req.service_id)
                
                review_data.append({
                    'id': review.id,
                    'rating': review.rating,
                    'remarks': review.remarks,
                    'date_created': review.date_created.isoformat(),
                    'customer_name': customer.customer_name if customer else 'Unknown Customer',
                    'service_name': service.name if service else 'Unknown Service'
                })
        
        return jsonify(review_data)
    except Exception as e:
        print(f"Error fetching professional reviews: {str(e)}")
        return jsonify({'error': 'Failed to fetch reviews'}), 500

@api.route('/professional/availability', methods=['PUT'])
@auth_required('token')
def update_professional_availability():
    try:
        # Ensure the current user is a professional
        if current_user.role != 'professional':
            return jsonify({'error': 'Unauthorized access'}), 403
            
        data = request.get_json()
        
        if 'is_available' not in data:
            return jsonify({'error': 'Missing is_available field'}), 400
            
        professional = ServiceProfessional.query.get(current_user.id)
        professional.is_available = data['is_available']
        
        db.session.commit()
        
        return jsonify({
            'message': f'Availability updated to {"available" if data["is_available"] else "unavailable"}',
            'is_available': professional.is_available
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error updating professional availability: {str(e)}")
        return jsonify({'error': 'Failed to update availability'}), 500

@api.route('/professional/requests/<int:request_id>/exit-location', methods=['POST'])
@auth_required('token')
def confirm_location_exit(request_id):
    try:
        # Ensure the current user is a professional
        if current_user.role != 'professional':
            return jsonify({'error': 'Unauthorized access'}), 403
            
        # Get the service request
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        # Ensure the request is assigned to this professional
        if service_request.professional_id != current_user.id:
            return jsonify({'error': 'This request is not assigned to you'}), 403
            
        # Update the request to mark location exit
        service_request.has_exited_location = True
        service_request.exited_at = db.func.current_timestamp()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Location exit confirmed',
            'id': service_request.id
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error confirming location exit: {str(e)}")
        return jsonify({'error': 'Failed to confirm location exit'}), 500

@api.route('/professional/available-requests', methods=['GET'])
@auth_required('token')
def get_available_service_requests():
    try:
        # Ensure the current user is a professional
        if current_user.role != 'professional':
            return jsonify({'error': 'Unauthorized access'}), 403
            
        # Get the professional record to check service type
        professional = ServiceProfessional.query.get(current_user.id)
        
        if not professional:
            return jsonify({'error': 'Professional profile not found'}), 404
            
        # Get service type of the professional
        service_type = professional.service_type
        
        if not service_type:
            return jsonify({'error': 'No service type defined for this professional'}), 400
            
        # Add debugging information
        print(f"Looking for available requests matching service type: {service_type}")
        
        # FLEXIBLE MATCHING: Find services that match the professional's specialty
        matching_services = Service.query.filter(
            # Changed from exact matching to pattern matching
            Service.category.ilike(f"%{service_type}%"), 
            Service.is_active == True
        ).all()
        
        # Debug service matching
        print(f"Found {len(matching_services)} matching services")
        for svc in matching_services:
            print(f"- Service ID: {svc.id}, Name: {svc.name}")
        
        if not matching_services:
            # Try even broader search - get all active services
            print("No service matches at all, showing all active services")
            matching_services = Service.query.filter_by(is_active=True).all()
            print(f"Found {len(matching_services)} active services total")
        
        # Get IDs of matching services
        service_ids = [service.id for service in matching_services]
        
        # Debug - List all service requests in the system
        all_pending = ServiceRequest.query.filter_by(status='pending').all()
        print(f"Total pending requests in system: {len(all_pending)}")
        
        # Find pending requests for these services that don't have a professional assigned yet
        pending_requests = ServiceRequest.query.filter(
            ServiceRequest.service_id.in_(service_ids) if service_ids else True,
            ServiceRequest.status == 'pending',
            ServiceRequest.professional_id.is_(None)
        ).all()
        
        print(f"Found {len(pending_requests)} matching pending requests")
        
        # Prepare response data
        result = []
        for req in pending_requests:
            # Get service details
            service = Service.query.get(req.service_id)
            # Get customer details
            customer = Customer.query.get(req.customer_id)
            
            # Don't include customer's personal information at this stage
            # Only include PIN code for location matching
            request_data = {
                'id': req.id,
                'status': req.status,
                'pin_code': req.pin_code,
                'created_at': req.created_at.isoformat() if req.created_at else None,
                'special_instructions': req.special_instructions,
                'service': {
                    'id': service.id,
                    'name': service.name,
                    'base_price': service.base_price,
                    'description': service.description,
                    'category': service.category
                } if service else None,
                'customer': {
                    'customer_name': 'Customer'  # Omit personal details until accepted
                }
            }
            
            result.append(request_data)
            
        return jsonify(result)
    except Exception as e:
        print(f"Error fetching available service requests: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to fetch available service requests'}), 500

# Add a new debug endpoint to see ALL pending requests
@api.route('/professional/all-pending-requests', methods=['GET'])
@auth_required('token')
def get_all_pending_requests():
    try:
        # Only professionals can access this
        if current_user.role != 'professional':
            return jsonify({'error': 'Unauthorized access'}), 403
            
        # Get ALL pending requests regardless of service type
        all_pending = ServiceRequest.query.filter_by(status='pending').all()
        
        result = []
        for req in all_pending:
            # Get service details
            service = Service.query.get(req.service_id)
            # Get customer details
            customer = Customer.query.get(req.customer_id)
            
            request_data = {
                'id': req.id,
                'status': req.status,
                'pin_code': req.pin_code,
                'created_at': req.created_at.isoformat() if req.created_at else None,
                'special_instructions': req.special_instructions,
                'service_id': req.service_id,
                'customer_id': req.customer_id,
                'professional_id': req.professional_id,
                'service_info': {
                    'name': service.name if service else 'Unknown',
                    'category': service.category if service else 'Unknown'
                },
                'customer_info': {
                    'name': customer.customer_name if customer else 'Unknown'
                }
            }
            
            result.append(request_data)
            
        return jsonify({
            'total_count': len(result),
            'requests': result
        })
    except Exception as e:
        print(f"Error in get_all_pending_requests: {str(e)}")
        return jsonify({'error': str(e)}), 500

#cust is the shortform for customer

cust = Blueprint('cust', __name__, url_prefix='/api/cust')

# Customer routes
@api.route('/customer/requests', methods=['POST'])
@auth_required('token')
def create_service_request():
    try:
        # Ensure the current user is a customer
        if current_user.role != 'customer':
            return jsonify({'error': 'Only customers can create service requests'}), 403
            
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Validate required fields
        if not data.get('pin_code'):
            return jsonify({'error': 'PIN code is required'}), 400
            
        # Get service ID (either directly provided or look up by category)
        service_id = data.get('service_id')
        category = data.get('category')
        
        print(f"Received request: service_id={service_id}, category={category}, pin_code={data.get('pin_code')}")
        
        # If no service_id but category is provided, find the first active service in that category
        if not service_id and category:
            # Add debug logging
            print(f"Looking up service by category: {category}")
            
            # Create a default service if none exists
            service = Service.query.filter_by(category=category, is_active=True).first()
            
            if not service:
                print(f"No active service found for category '{category}', creating one...")
                # Create a default service for this category if none exists
                try:
                    # Get admin user for the service creation
                    admin = User.query.filter_by(role='admin').first()
                    admin_id = None
                    if admin:
                        admin_record = Admin.query.get(admin.id)
                        if not admin_record:
                            admin_record = Admin(id=admin.id)
                            db.session.add(admin_record)
                            db.session.flush()
                        admin_id = admin_record.id
                    
                    # Create a new service
                    service = Service(
                        name=f"{category} Service",
                        description=f"Standard {category} service",
                        base_price=500,  # Default price
                        time_required=60,  # Default time (1 hour)
                        category=category,
                        is_active=True,
                        created_by_admin_id=admin_id
                    )
                    db.session.add(service)
                    db.session.flush()
                    print(f"Created new service: {service.name} (ID: {service.id})")
                except Exception as e:
                    print(f"Failed to create service: {str(e)}")
                    return jsonify({'error': f'Cannot create service for category: {category}. Please contact support.'}), 500
            
            if service:
                service_id = service.id
                print(f"Found/created service: {service.name} (ID: {service_id}) in category {category}")
            else:
                return jsonify({'error': f'No service found in category: {category}. Please try a different category or contact support.'}), 404
                
        if not service_id:
            return jsonify({'error': 'Service ID or category is required'}), 400
        
        # Create service request
        service_request = ServiceRequest(
            customer_id=current_user.id,
            service_id=service_id,
            pin_code=data.get('pin_code'),
            special_instructions=data.get('special_instructions', ''),
            status='pending',
            created_at=db.func.current_timestamp()
        )
        
        db.session.add(service_request)
        db.session.commit()
        
        return jsonify({
            'message': 'Service request created successfully',
            'request_id': service_request.id,
            'status': service_request.status
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating service request: {str(e)}")
        return jsonify({'error': 'Failed to create service request'}), 500

@api.route('/customer/requests', methods=['GET'])
@auth_required('token')
def get_customer_requests():
    try:
        # Ensure the current user is a customer
        if current_user.role != 'customer':
            return jsonify({'error': 'Unauthorized access'}), 403
            
        # Get all requests for this customer
        requests = ServiceRequest.query.filter_by(customer_id=current_user.id).all()
        
        # Prepare response data
        result = []
        for req in requests:
            # Get service details
            service = Service.query.get(req.service_id)
            
            # Get professional details if assigned
            professional = None
            if req.professional_id:
                professional = ServiceProfessional.query.get(req.professional_id)
                
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
                } if service else None,
                'professional': {
                    'id': professional.id,
                    'professional_name': professional.professional_name,
                    'service_type': professional.service_type,
                    'experience': professional.experience
                } if professional else None,
                'has_review': review is not None
            }
            
            result.append(request_data)
            
        return jsonify(result)
        
    except Exception as e:
        print(f"Error fetching customer requests: {str(e)}")
        return jsonify({'error': 'Failed to fetch customer requests'}), 500

@api.route('/customer/services', methods=['GET'])
def get_available_services():
    try:
        # Get all active services
        services = Service.query.filter_by(is_active=True).all()
        
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
            
        return jsonify(result)
    except Exception as e:
        print(f"Error fetching services: {str(e)}")
        return jsonify({'error': 'Failed to fetch services'}), 500

@api.route('/professional/profile', methods=['GET', 'PUT'])
@auth_required('token')
def professional_profile():
    try:
        # Ensure the current user is a professional
        if current_user.role != 'professional':
            return jsonify({'error': 'Unauthorized access'}), 403
            
        # Get the professional's profile
        professional = ServiceProfessional.query.get(current_user.id)
        
        if not professional:
            return jsonify({'error': 'Professional profile not found'}), 404
        
        if request.method == 'GET':
            # Return profile data
            result = {
                'id': professional.id,
                'professional_name': professional.professional_name,
                'service_type': professional.service_type,
                'description': professional.description,
                'experience': professional.experience,
                'is_approved': professional.is_approved,
                'approval_date': professional.approval_date.isoformat() if professional.approval_date else None,
                'average_rating': professional.average_rating,
                'total_reviews': professional.total_reviews,
                'email': professional.email,
                'phone': professional.phone
            }
            
            return jsonify(result)
        elif request.method == 'PUT':
            # Update profile data
            data = request.get_json()
            
            if data:
                if 'description' in data:
                    professional.description = data['description']
                if 'phone' in data:
                    professional.phone = data['phone']
                if 'experience' in data and data['experience'] is not None:
                    try:
                        professional.experience = int(data['experience'])
                    except (ValueError, TypeError):
                        return jsonify({'error': 'Experience must be a number'}), 400
                
                db.session.commit()
                
                # Return updated profile data
                return jsonify({
                    'message': 'Profile updated successfully',
                    'id': professional.id,
                    'professional_name': professional.professional_name,
                    'description': professional.description,
                    'phone': professional.phone,
                    'experience': professional.experience
                })
            else:
                return jsonify({'error': 'No data provided'}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error in professional_profile: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@api.route('/debug/professional/assignments', methods=['GET'])
@auth_required('token')
def debug_professional_assignments():
    """Debug endpoint to check response format for professional assignments"""
    try:
        # Ensure the current user is a professional
        if current_user.role != 'professional':
            return jsonify({'error': 'Unauthorized access'}), 403
            
        # Get all requests for this professional
        service_requests = ServiceRequest.query.filter_by(professional_id=current_user.id).all()
        
        # Prepare response data
        result = []
        for req in service_requests:
            # Get service details
            service = Service.query.get(req.service_id)
            # Get customer details
            customer = Customer.query.get(req.customer_id)
            
            # Create the request data with consistent format
            request_data = {
                'id': req.id,
                'status': req.status,
                'pin_code': req.pin_code,
                'created_at': req.created_at.isoformat() if req.created_at else None,
                'accepted_at': req.accepted_at.isoformat() if req.accepted_at else None,
                'completed_at': req.completed_at.isoformat() if req.completed_at else None,
                'closed_at': req.closed_at.isoformat() if req.closed_at else None,
                'special_instructions': req.special_instructions,
                'final_amount': req.final_amount if req.final_amount else 0,
                'service': {
                    'id': service.id,
                    'name': service.name,
                    'base_price': service.base_price,
                    'description': service.description
                } if service else None,
                'customer': {
                    'id': customer.id,
                    'customer_name': customer.customer_name,
                    'phone': customer.phone,
                    'address': customer.address
                } if customer else None
            }
            
            result.append(request_data)
            
        # Also log the result for server-side debugging
        print(f"Debug professional assignments: Found {len(result)} assignments")
        
        return jsonify({
            'count': len(result),
            'data': result
        })
    except Exception as e:
        print(f"Debug error in assignments: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Add this new endpoint for rejection reasons
@api.route('/professional/requests/<int:request_id>/reject-reason', methods=['POST', 'OPTIONS'])
@auth_required('token')
def add_rejection_reason(request_id):
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authentication-Token')
        return response
        
    try:
        # Ensure the current user is a professional
        if current_user.role != 'professional':
            return jsonify({'error': 'Unauthorized access'}), 403
            
        # Get the service request
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        # Check if this is a valid request for the professional
        if service_request.professional_id is not None and service_request.professional_id != current_user.id:
            return jsonify({'error': 'This request is not assigned to you'}), 403
            
        # Get the rejection reason from the request data
        data = request.get_json()
        if not data or 'reason' not in data:
            return jsonify({'error': 'Rejection reason is required'}), 400
            
        # Update the request with the rejection reason
        service_request.rejection_reason = data['reason']
        db.session.commit()
        
        return jsonify({
            'message': 'Rejection reason added successfully',
            'id': service_request.id,
            'status': service_request.status,
            'rejection_reason': service_request.rejection_reason
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error adding rejection reason: {str(e)}")
        return jsonify({'error': f'Failed to add rejection reason: {str(e)}'}), 500

# Define the Customer blueprint once - but use the API blueprint for consistency
cust = Blueprint('cust', __name__, url_prefix='/api/cust')
# We're not actually using the cust blueprint currently, keeping it for future use

# Customer routes are properly defined in the api blueprint - NO DUPLICATES BELOW THIS LINE

@api.route('/customer/requests/<int:request_id>/review', methods=['POST'])
@auth_required('token')
def submit_service_review(request_id):
    try:
        # Ensure the current user is a customer
        if current_user.role != 'customer':
            return jsonify({'error': 'Unauthorized access'}), 403
            
        # Get the service request
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        # Ensure the request belongs to this customer
        if service_request.customer_id != current_user.id:
            return jsonify({'error': 'This request is not associated with your account'}), 403
            
        # Check if the service is completed
        if service_request.status != 'completed':
            return jsonify({'error': 'You can only review completed services'}), 400
            
        # Check if review already exists
        existing_review = Reviews.query.filter_by(service_request_id=request_id).first()
        if existing_review:
            return jsonify({'error': 'You have already reviewed this service'}), 400
            
        # Get data from request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Validate rating
        rating = data.get('rating')
        if rating is None:
            return jsonify({'error': 'Rating is required'}), 400
            
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Rating must be a number between 1 and 5'}), 400
            
        # Create review - remove professional_id if it's not a valid field
        # and rely on service_request_id to link to the professional
        review = Reviews(
            customer_id=current_user.id,
            service_request_id=request_id,
            rating=rating,
            remarks=data.get('remarks', ''),
            date_created=db.func.current_timestamp()
        )
        
        db.session.add(review)
        
        # Mark the service request as reviewed
        service_request.is_reviewed = True
        service_request.closed_at = db.func.current_timestamp()
        
        # Update professional's average rating if there is a professional assigned
        if service_request.professional_id:
            professional = ServiceProfessional.query.get(service_request.professional_id)
            if professional:
                # If this is the first review, set it as the average
                if professional.total_reviews == 0:
                    professional.average_rating = rating
                    professional.total_reviews = 1
                else:
                    # Calculate new average rating
                    total_points = professional.average_rating * professional.total_reviews
                    new_total = total_points + rating
                    professional.total_reviews += 1
                    professional.average_rating = new_total / professional.total_reviews
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review submitted successfully',
            'review_id': review.id,
            'rating': review.rating
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error submitting review: {str(e)}")
        return jsonify({'error': f'Failed to submit review: {str(e)}'}), 500
    

# @api.route('/api/export')
# def exprt_csv():
#     result = csv_report.delay()  #async object
#     return jsonify({
#         'id': result.id,
#         'result': result.get(timeout=1) if result.ready() else None
#     })

# @api.route('/api/csv_result/<id>')
# def csv_result(id):
#     result = AsyncResult(id)
    
#     return jsonify({
#         "ready": result.ready(),
#         "successful": result.successful(),
#         "value": result.result if result.successful() else None
#     })

from flask import Blueprint, jsonify, request
from application.models import db, User, ServiceProfessional, Service, Customer
from application.auth import admin_required, user_datastore
from flask_security import auth_required, login_required, hash_password
import uuid
# from app import create_app as app
# from app import create_app

# app = create_app()  # Now, app is a Flask instance

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/api/admin', methods=['GET'])
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

@admin.route('/api/admin/services/<int:service_id>', methods=['PUT', 'DELETE'])
@auth_required('token')
@admin_required
def service_operations(service_id):
    service = Service.query.get_or_404(service_id)
    
    if request.method == 'DELETE':
        db.session.delete(service)
        db.session.commit()
        return jsonify({'message': 'Service deleted successfully'})
    
    data = request.get_json()
    service.name = data.get('name', service.name)
    service.base_price = data.get('base_price', service.base_price)
    db.session.commit()
    return jsonify({'message': 'Service updated successfully'})

# Create a new blueprint for authentication
auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register/customer', methods=['POST'])
def register_customer():
    try:
        data = request.get_json()
        
        # Check if user already exists
        if user_datastore.find_user(email=data['email']):
            return jsonify({'message': 'Email already registered'}), 400     #400 is bad request
        
        # Create new customer
        customer = Customer(
            username=data['username'],
            email=data['email'],
            password=hash_password(data['password']),
            fs_uniquifier=str(uuid.uuid4()),
            active=True,
            role='customer',
            # display_name=data['name'],
            customer_name=data['name'],
            phone=data['phone'],
            address=data['address'],
            pin_code=data['pin_code']
        )
        
        db.session.add(customer)
        db.session.commit()
        
        # Add customer role
        customer_role = user_datastore.find_role('customer')
        user_datastore.add_role_to_user(customer, customer_role)
        db.session.commit()
        
        return jsonify({
            'message': 'Customer registered successfully',
            'user_id': customer.id
        }), 201                                                             #201 is created
        
    except KeyError as e:
        return jsonify({'message': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500

@auth.route('/register/professional', methods=['POST'])
def register_professional():
    try:
        data = request.get_json()
        
        # Check if user already exists
        if user_datastore.find_user(email=data['email']):
            return jsonify({'message': 'Email already registered'}), 400
        
        # Create new service professional
        professional = ServiceProfessional(
            username=data['username'],
            email=data['email'],
            password=hash_password(data['password']),
            fs_uniquifier=str(uuid.uuid4()),
            active=True,
            role='professional',
            display_name=data['name'],
            professional_name=data['name'],
            description=data.get('description'),
            service_type=data['service_type'],
            experience=data['experience'],
            documents=data.get('documents', {}),
            is_approved=False
        )
        
        db.session.add(professional)
        db.session.commit()
        
        # Add professional role
        professional_role = user_datastore.find_role('professional')
        user_datastore.add_role_to_user(professional, professional_role)
        db.session.commit()
        
        return jsonify({
            'message': 'Professional registered successfully. Waiting for admin approval.',
            'user_id': professional.id
        }), 201
        
    except KeyError as e:
        return jsonify({'message': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500 
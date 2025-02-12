from flask import Blueprint, jsonify, request
from application.models import db, User, ServiceProfessional, Service, Customer
from application.auth import admin_required
from flask_security import auth_required

admin = Blueprint('admin', __name__)

@admin.route('/api/admin/users', methods=['GET'])
@auth_required()
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
@auth_required()
@admin_required
def approve_professional(prof_id):
    professional = ServiceProfessional.query.get_or_404(prof_id)
    professional.is_approved = True
    db.session.commit()
    return jsonify({'message': 'Professional approved successfully'})

@admin.route('/api/admin/users/<int:user_id>/toggle-block', methods=['POST'])
@auth_required()
@admin_required
def toggle_block_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_blocked = not user.is_blocked
    db.session.commit()
    return jsonify({
        'message': f'User {"blocked" if user.is_blocked else "unblocked"} successfully'
    })

@admin.route('/api/admin/services', methods=['GET', 'POST'])
@auth_required()
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
@auth_required()
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
# transactio based CRUD api will be here

from flask_restful import Api, Resource, reqparse, fields, marshal_with
from backend.application.models import *
from flask_security import auth_required, current_user, roles_required
from flask import jsonify, request
from backend.application.auth import admin_required, customer_required, professional_required

api = Api()

# Define response fields for each model
customer_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'customer_name': fields.String,
    'phone': fields.String,
    'address': fields.String,
    'pin_code': fields.String,
    'is_blocked': fields.Boolean,
    'date_created': fields.DateTime(dt_format='iso8601')
}

service_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'base_price': fields.Float,
    'category': fields.String,
    'time_required': fields.Integer,
    'is_active': fields.Boolean,
    'availability': fields.String
}

service_request_fields = {
    'id': fields.Integer,
    'service': fields.Nested({'id': fields.Integer, 'name': fields.String}),
    'status': fields.String,
    'pin_code': fields.String,
    'created_at': fields.DateTime(dt_format='iso8601'),
    'special_instructions': fields.String,
    'professional': fields.Nested({
        'id': fields.Integer,
        'professional_name': fields.String
    }, allow_null=True)
}

professional_fields = {
    'id': fields.Integer,
    'professional_name': fields.String,
    'service_type': fields.String,
    'experience': fields.Integer,
    'is_approved': fields.Boolean,
    'average_rating': fields.Float,
    'total_reviews': fields.Integer,
    'description': fields.String
}

review_fields = {
    'id': fields.Integer,
    'rating': fields.Integer,
    'remarks': fields.String,
    'date_created': fields.DateTime(dt_format='iso8601'),
    'customer_id': fields.Integer
}

# Customer Resources
class CustomerAPI(Resource):
    @auth_required('token')
    @customer_required
    @marshal_with(customer_fields)
    def get(self):                    #self because we r using class method
        """Get customer profile"""
        return Customer.query.get(current_user.id)

    @auth_required('token')
    @customer_required
    @marshal_with(customer_fields)
    def put(self):
        """Update customer profile"""
        parser = reqparse.RequestParser()
        parser.add_argument('phone', type=str)
        parser.add_argument('address', type=str)
        parser.add_argument('pin_code', type=str)
        args = parser.parse_args()     #the data that we get from the request in JSON format(backend)  is now stored in argsin dictionary format(backend)

        customer = Customer.query.get(current_user.id)      
        for key, value in args.items():
            if value is not None:
                setattr(customer, key, value)
        
        db.session.commit()
        return customer

# Service Resources
class ServicesAPI(Resource):
    @marshal_with(service_fields)
    def get(self):
        """Get all available services"""
        return Service.query.filter_by(is_active=True).all()

class ServiceByLocationAPI(Resource):
    @marshal_with(service_fields)
    def get(self, pin_code):
        """Get services available in specific location"""
        # Here you could add logic to filter services by location
        return Service.query.filter_by(is_active=True).all()

# Service Request Resources
class ServiceRequestAPI(Resource):
    @auth_required('token')
    @customer_required
    @marshal_with(service_request_fields)
    def post(self):
        """Create new service request"""
        parser = reqparse.RequestParser()
        parser.add_argument('service_id', type=int, required=True)
        parser.add_argument('pin_code', type=str, required=True)
        parser.add_argument('special_instructions', type=str)
        args = parser.parse_args()

        service_request = ServiceRequest(
            customer_id=current_user.id,
            service_id=args['service_id'],
            pin_code=args['pin_code'],
            special_instructions=args.get('special_instructions')
        )
        db.session.add(service_request)
        db.session.commit()
        return service_request, 201

    @auth_required('token')
    @customer_required
    @marshal_with(service_request_fields)
    def get(self):
        """Get customer's service requests"""
        return ServiceRequest.query.filter_by(customer_id=current_user.id).all()

# Professional Resources
class ProfessionalAPI(Resource):
    @auth_required('token')
    @professional_required
    @marshal_with(professional_fields)
    def get(self):
        """Get professional's profile and assignments"""
        return ServiceProfessional.query.get(current_user.id)

    @auth_required('token')
    @professional_required
    @marshal_with(professional_fields)
    def put(self):
        """Update professional's profile"""
        parser = reqparse.RequestParser()
        parser.add_argument('service_type', type=str)
        parser.add_argument('experience', type=int)
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        prof = ServiceProfessional.query.get(current_user.id)
        for key, value in args.items():
            if value is not None:
                setattr(prof, key, value)
        
        db.session.commit()
        return prof

# Review Resources
class ReviewAPI(Resource):
    @auth_required('token')
    @customer_required
    @marshal_with(review_fields)
    def post(self, request_id):
        """Add review for completed service"""
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=int, required=True)
        parser.add_argument('remarks', type=str, required=True)
        args = parser.parse_args()

        service_request = ServiceRequest.query.get_or_404(request_id)
        if service_request.customer_id != current_user.id:
            return {
                'message': 'Unauthorized'
                }, 403
        if service_request.status != 'completed':
            return {
                'message': 'Can only review completed services'
                }, 400

        review = Reviews(
            service_request_id=request_id,
            customer_id=current_user.id,
            rating=args['rating'],
            remarks=args['remarks']
        )
        db.session.add(review)
        db.session.commit()
        return review

# User Resources
class UserList(Resource):
    @roles_required('admin')
    def get(self):
        users = User.query.all()
        return jsonify([{
            'id': user.id,
            'name': f"{user.first_name} {user.last_name}",
            'email': user.email,
            'role': 'professional' if isinstance(user, ServiceProfessional) else 'customer',
            'is_active': user.is_active,
            'is_approved': user.is_approved if isinstance(user, ServiceProfessional) else None
        } for user in users])

class UserAction(Resource):
    @roles_required('admin')
    def post(self, user_id, action):
        user = User.query.get_or_404(user_id)
        
        if action == 'approve':
            if not isinstance(user, ServiceProfessional):
                return {'message': 'User is not a service professional'}, 400
            user.is_approved = True
            db.session.commit()
            return {'message': 'Professional approved successfully'}
        
        elif action == 'toggle-status':
            user.is_active = not user.is_active
            db.session.commit()
            return {'message': f"User {'activated' if user.is_active else 'deactivated'} successfully"}
        
        return {'message': 'Invalid action'}, 400

class ServiceList(Resource):
    @roles_required('admin')
    def get(self):
        services = Service.query.all()
        return jsonify([{
            'id': service.id,
            'name': service.name,
            'price': service.price,
            'time_required': service.time_required,
            'description': service.description
        } for service in services])

    @roles_required('admin')
    def post(self):
        data = request.get_json()
        service = Service(
            name=data['name'],
            price=data['price'],
            time_required=data['time_required'],
            description=data['description']
        )
        db.session.add(service)
        db.session.commit()
        return {'message': 'Service created successfully', 'id': service.id}

class ServiceDetail(Resource):
    @roles_required('admin')
    def put(self, service_id):
        service = Service.query.get_or_404(service_id)
        data = request.get_json()
        
        service.name = data['name']
        service.price = data['price']
        service.time_required = data['time_required']
        service.description = data['description']
        
        db.session.commit()
        return {'message': 'Service updated successfully'}

    @roles_required('admin')
    def delete(self, service_id):
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        return {'message': 'Service deleted successfully'}

# Register resources
def initialize_routes(api):
    api.add_resource(CustomerAPI, '/api/customer/profile')
    api.add_resource(ServicesAPI, '/api/services')
    api.add_resource(ServiceByLocationAPI, '/api/services/<string:pin_code>')
    api.add_resource(ServiceRequestAPI, '/api/service-requests')
    api.add_resource(ProfessionalAPI, '/api/professional/profile')
    api.add_resource(ReviewAPI, '/api/service-requests/<int:request_id>/review')
    api.add_resource(UserList, '/api/users')
    api.add_resource(UserAction, '/api/users/<int:user_id>/<string:action>')
    api.add_resource(ServiceDetail, '/api/services/<int:service_id>')

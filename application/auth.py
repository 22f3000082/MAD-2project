from flask import current_app
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from application.models import db, User, Role
from functools import wraps
from flask_security import roles_required, current_user
from flask import abort

# Initialize Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

def init_security(app):
    security = Security(app, user_datastore)
    
    # Create default roles and admin user
    with app.app_context():
        # Create roles if they don't exist
        user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_datastore.find_or_create_role(name='professional', description='Service Professional')
        user_datastore.find_or_create_role(name='customer', description='Customer')
        
        db.session.commit()
        
        # Create default admin if it doesn't exist
        if not user_datastore.get_user('admin@example.com'):
            user_datastore.create_user(
                username='admin',
                email='admin@example.com',
                password=hash_password('admin123'),  # Change this in production!
                role='admin'
            )
            admin_user = user_datastore.get_user('admin@example.com')
            admin_role = user_datastore.find_role('admin')
            user_datastore.add_role_to_user(admin_user, admin_role)
            db.session.commit()

# Custom decorators for role-based access
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.has_role('admin'):
            abort(403)
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
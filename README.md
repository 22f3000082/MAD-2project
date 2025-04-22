# Household Services Management Application

This is a Progressive Web Application (PWA) for managing household services, connecting customers with service professionals, and providing administrative tools for monitoring and managing the platform.

## Features

### User Roles
- **Customers**: Can browse services, request service appointments, and leave reviews.
- **Professionals**: Can accept service requests, manage their schedule, and view their ratings.
- **Admins**: Can manage users, services, and view analytics about platform usage.

### Key Features
- User authentication and role-based access control
- Request and booking management system
- Reviews and ratings for professionals
- Progressive Web App capabilities for mobile use
- Responsive design for all device sizes

## Technical Stack

### Frontend
- Vue.js 3 with Vue Router and Vuex
- Bootstrap 5 for responsive UI
- Chart.js for data visualization
- Progressive Web App capabilities

### Backend
- Flask (Python) with RESTful API
- SQLAlchemy ORM
- Flask-Security for authentication
- Celery for background tasks (CSV generation)

## Getting Started

### Prerequisites
- Node.js and npm
- Python 3.8 or higher
- Redis (for Celery)

### Installation

1. Clone the repository
```
git clone https://github.com/yourusername/household-services.git
cd household-services
```

2. Set up the backend
```
cd backend
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
flask run
```

3. Set up the frontend
```
cd frontend
npm install
npm run serve
```

4. Access the application
- Frontend: http://localhost:8080
- Backend API: http://localhost:5000

## Development

### Key Directories
- `frontend/src/views/`: Vue components for each page
- `frontend/src/components/`: Reusable Vue components
- `frontend/src/services/`: API service modules
- `backend/application/`: Flask application modules
- `backend/application/routes.py`: API endpoints

## License
This project is licensed under the MIT License - see the LICENSE file for details. 

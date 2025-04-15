from flask import Flask, jsonify
from flask_mail import Mail
from .mail import init_mail
import requests

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USERNAME'] = 'houseservices@gmail.com'  # Ensure this is set correctly
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False

# Initialize Flask-Mail
init_mail(app)

# @app.route('/test-api', methods=['GET'])
# def test_api():
#     url = "http://localhost:8025/api/v2/users/jim"
#     response = requests.get(url)

#     if response.status_code == 200:
#         return jsonify({"success": True, "data": response.json()})
#     else:
#         return jsonify({"success": False, "error": response.text}), response.status_code

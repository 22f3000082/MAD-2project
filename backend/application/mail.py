from email import encoders
from jinja2 import Template
from flask_mail import Mail, Message
from flask import current_app

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# SMTP Configuration (Update these values)
SMTP_SERVER_HOST = 'localhost'
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "houseservices@gmail.com"
SENDER_PASSWORD = None

# Initialize Flask-Mail instance
mail = Mail()

def init_mail(app):
    """
    Initialize Flask-Mail with the given Flask app.
    """
    mail.init_app(app)

def send_email(to_address, subject, message, content="text"):
    """
    Sends an email using direct SMTP
    
    Args:
        to_address: Recipient email address
        subject: Email subject
        message: Message content
        content: Type of content ('text' or 'html')
    """
    try:
        # Create message container
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = SENDER_ADDRESS
        msg['To'] = to_address
        
        # Set the appropriate message content
        if content == "html":
            part = MIMEText(message, 'html')
        else:
            part = MIMEText(message, 'plain')
        
        msg.attach(part)
        
        # Send the message via local SMTP server
        print(f"Connecting to SMTP: {SMTP_SERVER_HOST}:{SMTP_SERVER_PORT}")
        smtp = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
        smtp.send_message(msg)
        smtp.quit()
        
        print(f"Email sent successfully to {to_address}")
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False


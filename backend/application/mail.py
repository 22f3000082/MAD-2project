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

def send_email(to_address, subject, message, content="text"):
    """
    Sends an email using Flask-Mail
    
    Args:
        to_address: Recipient email address
        subject: Email subject
        message: Message content
        content: Type of content ('text' or 'html')
    """
    try:
        # Import mail extension inside the function to avoid circular imports
        from run import mail
        
        msg = Message(
            subject=subject,
            recipients=[to_address]
        )
        
        # Set the appropriate message content
        if content == "html":
            msg.html = message
        else:
            msg.body = message
            
        print(f"Sending email to {to_address}: {subject}")
        mail.send(msg)
        print(f"Email sent successfully to {to_address}")
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False


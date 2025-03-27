from email import encoders
from jinja2 import Template
from flask_mail import Mail

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# SMTP Configuration (Update these values)
SMTP_SERVER_HOST = "smtp.yourmailserver.com"
SMTP_SERVER_PORT = 587
SENDER_ADDRESS = "noreply@yourapp.com"
SENDER_PASSWORD = "your-email-password"

def send_email(to_address, subject, message, content="html", attachment_file=None):
    """
    Sends an email with optional HTML content and an attachment.
    """
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    # Attach the email body
    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))

    # Attach a file if provided
    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={attachment_file.split('/')[-1]}")
        msg.attach(part)

    # Send email using SMTP
    try:
        server = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
        server.starttls()
        server.login(SENDER_ADDRESS, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


from celery import shared_task, Celery
from .models import User, ServiceProfessional, Service, ServiceRequest, Reviews, Role, BlockedUsers
import time
# import datetime
import csv
from flask_mail import Mail, Message
from jinja2 import Template
from flask import render_template
from celery.schedules import crontab
from datetime import datetime
from flask import render_template
from .mail import send_email  # Import the email utility
import os  # Add this import



celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')
celery.conf.timezone = "Asia/Kolkata"
celery.conf.broker_connection_retry_on_startup = True
celery.conf.task_serializer = 'json'
celery.conf.result_serializer = 'json'
celery.conf.accept_content = ['json']
celery.conf.worker_hijack_root_logger = False
celery.conf.worker_redirect_stdouts = False


# mail = Mail()
#scheduled tasks
@celery.task(ignore_results=False, name='backend.application.task.monthly_report')
def monthly_report():
    """Scheduled task to send monthly reports to customers."""
    try:
        from flask import current_app
        with current_app.app_context():
            # Set the template folder explicitly
            TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
            current_app.template_folder = TEMPLATE_DIR
            print(f"Resolved TEMPLATE_DIR: {TEMPLATE_DIR}")

            # Configure mail settings explicitly for this app context
            current_app.config['MAIL_SERVER'] = 'localhost'
            current_app.config['MAIL_PORT'] = 1025
            current_app.config['MAIL_USERNAME'] = 'houseservices@gmail.com'
            current_app.config['MAIL_PASSWORD'] = None
            current_app.config['MAIL_USE_TLS'] = False
            current_app.config['MAIL_USE_SSL'] = False
            
            # Initialize mail with the current app
            from .mail import init_mail
            init_mail(current_app)

            customers = User.query.filter_by(role='customer').all()
            report_date = datetime.now().strftime('%B %Y')
            
            print(f"Generating monthly reports for {len(customers)} customers")
            
            for customer in customers:
                try:
                    # Get user activity data
                    services_requested = ServiceRequest.query.filter_by(customer_id=customer.id).count()
                    services_closed = ServiceRequest.query.filter_by(customer_id=customer.id, status='pending').count()
                    
                    # Render HTML report
                    report_html = render_template(
                        'mail_details.html',
                        customer_name=customer.username,
                        services_requested=services_requested,
                        services_closed=services_closed,
                        report_date=report_date
                    )
                    
                    # Send email
                    from .mail import send_email
                    success = send_email(
                        to_address=customer.email,
                        subject=f"Your Monthly Service Report - {report_date}",
                        message=report_html,
                        content="html"
                    )
                    
                    if success:
                        print(f"Email sent to {customer.email}")
                    else:
                        print(f"Failed to send email to {customer.email}")
                        
                except Exception as customer_error:
                    print(f"Error processing customer {customer.id}: {str(customer_error)}")
                    continue
                    
            return "Monthly reports sent."
    except Exception as e:
        print(f"Error in monthly_report task: {str(e)}")
        return f"Error: {str(e)}"

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/2'),  # Runs every 2 minutes
        monthly_report.s(),
    )
# # Schedule the task to run on the first of every month
# from celery.schedules import crontab

# celery.conf.beat_schedule = {
#     'send-monthly-report': {
#         'task': 'tasks.monthly_report',
#         'schedule': crontab(minute=0, hour=0, day_of_month=1),
#     },
# }
    
# # Schedule the task to run on the first of every month
# celery.conf.beat_schedule = {
#     'send-monthly-report': {
#         'task': 'tasks.send_monthly_report',
#         'schedule': crontab(minute=0, hour=0, day_of_month=1),
#     },
# }


#User Triggered Tasks

@celery.task(ignore_results=False, name='download_csv_report')
def download_csv_report():


    try:
        print("Starting CSV report generation...")

        # Ensure app context is available for DB queries
        # We need to tell Celery to use the Flask app context
        # so that we can access the database, etc.
        from flask import current_app
        with current_app.app_context():
            # Get a list of all users and service requests
            users = User.query.all()
            service_rqst = ServiceRequest.query.all()

            # Create a timestamped filename
            # filename = f"service_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # filename = os.path.join("static", filename)
            filename = f"service_report_{timestamp}.csv"

            
            import os
            # PROJECT_ROOT = os.path.abspath(os.path.join(current_app.root_path, ".."))  # Go two levels up
            # PROJECT_ROOT = r"C:/Users/91829/OneDrive/Documents/VS CODE/Household_service_22f3000082"
            PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            static_dir = os.path.join(PROJECT_ROOT, 'static')
            # static_dir = os.path.join(current_app.root_path, 'static')
            os.makedirs(static_dir, exist_ok=True)  # Ensure directory exists
            # Debugging: Print paths
            print("Project Root:", PROJECT_ROOT)
            print("Static Dir:", static_dir)
                        
            file_path = os.path.join(static_dir, filename)

            
            print(f"Saving CSV to: {file_path}")

            # Open the file in write mode and create a CSV writer
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)

                # Write the header row
                writer.writerow(["Sr. No.", "Service ID", "Customer ID", "Professional ID", "Date", "Status"])

                # Write each row of the report
                for i, sr in enumerate(service_rqst, 1):
                    writer.writerow([i, sr.service_id, sr.customer_id, sr.professional_id, sr.created_at, sr.status])
            
            return filename  # Return filename instead of full path

    except Exception as e:
        print(f"CSV Generation Error: {str(e)}")
        return f"ERROR:{str(e)}"



#Scheduled Tasks

@shared_task(ignore_results = False, name = 'daily_remainder')
def daily_remainder():
    return "Daily Remainder Sent"

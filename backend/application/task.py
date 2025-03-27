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
from .mail import send_email  # Import the email utility


celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')
celery.conf.timezone = "Asia/Kolkata"
celery.conf.broker_connection_retry_on_startup = True
celery.conf.task_serializer = 'json'
celery.conf.result_serializer = 'json'
celery.conf.accept_content = ['json']
celery.conf.worker_hijack_root_logger = False
celery.conf.worker_redirect_stdouts = False


mail = Mail()
#scheduled tasks
@celery.task
# @shared_task(ignore_results = False, name = 'monthly_report')
def monthly_report():
    """Scheduled task to send monthly reports to customers."""
    with app.app_context():  # Ensure Flask context is available
        customers = User.query.filter_by(role='customer').all()
        report_date = datetime.utcnow().strftime('%B %Y')

        for customer in customers:
            services_requested = ServiceRequest.query.filter_by(user_id=customer.id).count()
            services_closed = ServiceRequest.query.filter_by(user_id=customer.id, status='pending').count()

            # Render HTML report
            report_html = render_template(
                'monthly_report.html',
                customer_name=customer.username,
                services_requested=services_requested,
                services_closed=services_closed,
                report_date=report_date
            )

            # Send email using the custom function
            send_email(
                to_address=customer.email,
                subject=f"Your Monthly Service Report - {report_date}",
                message=report_html,
                content="html"
            )

    return "Monthly reports sent."

# Schedule the task to run on the first of every month
from celery.schedules import crontab

celery.conf.beat_schedule = {
    'send-monthly-report': {
        'task': 'tasks.monthly_report',
        'schedule': crontab(minute=0, hour=0, day_of_month=1),
    },
}
    
# Schedule the task to run on the first of every month
celery.conf.beat_schedule = {
    'send-monthly-report': {
        'task': 'tasks.send_monthly_report',
        'schedule': crontab(minute=0, hour=0, day_of_month=1),
    },
}


#User Triggered Tasks
@celery.task(ignore_results=False, name='download_csv_report')
# @shared_task(ignore_results=False, name='download_csv_report')
# @shared_task(ignore_results=False, name='download_csv_report')
def download_csv_report():
    try:
        print("Starting CSV report generation...")

        # Ensure app context is available for DB queries
        from flask import current_app
        with current_app.app_context():
            users = User.query.all()
            service_rqst = ServiceRequest.query.all()

            # Create a timestamped filename
            # filename = f"service_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # filename = os.path.join("static", filename)
            filename = f"service_report_{timestamp}.csv"
            
            # Get absolute path to static directory
            import os
            static_dir = os.path.join(current_app.root_path, 'static')
            os.makedirs(static_dir, exist_ok=True)  # Ensure directory exists
            
            file_path = os.path.join(static_dir, filename)
            
            print(f"Saving CSV to: {file_path}")
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Sr. No.", "Service ID", "Customer ID", "Professional ID", "Date", "Status"])
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

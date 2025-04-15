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
import requests


celery = Celery('backend.application.tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')
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


@celery.task(ignore_results=False, name='backend.application.task.download_csv_report')
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

@celery.task(ignore_results = False, name = 'backend.application.task.daily_remainder')
def daily_remainder(service_request_id=None): 
    print(f"Received service_request_id: {service_request_id}")  # Debugging
    """Send a notification when a service request status changes."""
    try:
        # Validate we have a service request ID
        if not service_request_id:
            print("No service request ID provided, skipping notification")
            return "No service request ID provided"
            
        # Get the service request details
        from flask import current_app
        with current_app.app_context():
            from .models import ServiceRequest, Customer, ServiceProfessional, Service
            
            # Get the service request
            service_request = ServiceRequest.query.get(service_request_id)
            if not service_request:
                print(f"Service request {service_request_id} not found")
                return f"Service request {service_request_id} not found"
                
            
            # Get related data
            customer = Customer.query.get(service_request.customer_id) if service_request.customer_id else None
            professional = ServiceProfessional.query.get(service_request.professional_id) if service_request.professional_id else None
            service = Service.query.get(service_request.service_id) if service_request.service_id else None
            
            # Create a detailed message
            customer_name = customer.customer_name if customer else "Customer"
            professional_name = professional.professional_name if professional else "No professional assigned"
            service_name = service.name if service else "Unknown service"
            
            text = f"Service Request Update: ID #{service_request_id}\n" \
                   f"Status changed to: {service_request.status.upper()}\n" \
                   f"Customer: {customer_name}\n" \
                   f"Professional: {professional_name}\n" \
                   f"Service: {service_name}\n" \
                   f"Please check the status of your request at http://127.0.0.1:8080/login"
            
        webhook_url = "https://chat.googleapis.com/v1/spaces/AAAAESCrGdU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=FdeSsWeM_-F5kdvH8hMRy4uiidfTI9SDkCwfWMliIDI"
        
        # print(f"Sending reminder to Google Chat for {username}")
        print(f"Sending status change notification for request #{service_request_id}")
        response = requests.post(webhook_url, json={"text": text})
        
        # Check if the request was successful
        if response.status_code == 200:
            # print(f"Reminder sent successfully: {response.text}")
             print(f"Notification sent successfully: {response.text}")
        else:
            # print(f"Failed to send reminder. Status code: {response.status_code}, Response: {response.text}")
            print(f"Failed to send notification. Status code: {response.status_code}, Response: {response.text}")
        # return f"Daily Reminder Sent to {username}"
        return f"Status change notification sent for request #{service_request_id}"
    except Exception as e:
        # print(f"Error sending reminder: {str(e)}")
        print(f"Error sending notification: {str(e)}")
        return f"Error: {str(e)}"

# @celery.task(ignore_results=False, name='generate_monthly_pdf')
# def generate_monthly_pdf():
#     """Generate PDF report for monthly activities"""
#     try:
#         from flask import current_app
#         with current_app.app_context():
#             from reportlab.lib.pagesizes import letter
#             from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
#             from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
#             from reportlab.lib import colors
#             from dateutil.relativedelta import relativedelta
            
#             # Generate a unique filename
#             current_month = datetime.now().strftime("%B_%Y")
#             filename = f"Monthly_Activity_Report_{current_month}.pdf"
            
#             # Setup path for saving the file
#             import os
#             PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
#             static_dir = os.path.join(PROJECT_ROOT, 'static')
#             os.makedirs(static_dir, exist_ok=True)  # Ensure directory exists
            
#             filepath = os.path.join(static_dir, filename)
#             print(f"Saving PDF to: {filepath}")
            
#             # Create the PDF document
#             doc = SimpleDocTemplate(filepath, pagesize=letter)
#             styles = getSampleStyleSheet()
#             elements = []
            
#             # Title
#             title_style = styles["Heading1"]
#             title = Paragraph(f"Monthly Activity Report - {current_month}", title_style)
#             elements.append(title)
#             elements.append(Spacer(1, 12))
            
#             # Summary section
#             elements.append(Paragraph("Monthly Summary", styles["Heading2"]))
#             elements.append(Spacer(1, 6))
            
#             # Calculate date range for the previous month
#             today = datetime.now()
#             first_day = today.replace(day=1) - relativedelta(months=1)
#             last_day = today.replace(day=1) - relativedelta(days=1)
            
#             # Get statistics for the month
#             new_users = User.query.filter(
#                 User.date_created.between(first_day, last_day)
#             ).count() if hasattr(User, 'date_created') else User.query.count()
            
#             new_requests = ServiceRequest.query.filter(
#                 ServiceRequest.created_at.between(first_day, last_day)
#             ).count()
            
#             completed_requests = ServiceRequest.query.filter(
#                 ServiceRequest.status == 'completed',
#                 ServiceRequest.completed_at.between(first_day, last_day) if hasattr(ServiceRequest, 'completed_at') else True
#             ).count()
            
#             # Calculate total revenue
#             total_revenue = 0
#             completed_requests_list = ServiceRequest.query.filter_by(status='completed').all()
#             for req in completed_requests_list:
#                 if hasattr(req, 'final_amount') and req.final_amount:
#                     try:
#                         total_revenue += float(req.final_amount)
#                     except (ValueError, TypeError):
#                         pass
            
#             # Add summary table
#             summary_data = [
#                 ["Metric", "Value"],
#                 ["New Users", str(new_users)],
#                 ["Service Requests", str(new_requests)],
#                 ["Completed Requests", str(completed_requests)],
#                 ["Total Revenue", f"₹{total_revenue:.2f}"]
#             ]
            
#             summary_table = Table(summary_data, colWidths=[300, 200])
#             summary_table.setStyle(TableStyle([
#                 ('BACKGROUND', (0, 0), (1, 0), colors.grey),
#                 ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
#                 ('ALIGN', (0, 0), (1, 0), 'CENTER'),
#                 ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
#                 ('FONTSIZE', (0, 0), (1, 0), 14),
#                 ('BOTTOMPADDING', (0, 0), (1, 0), 12),
#                 ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                 ('GRID', (0, 0), (-1, -1), 1, colors.black)
#             ]))
#             elements.append(summary_table)
#             elements.append(Spacer(1, 12))
            
#             # Top services section
#             elements.append(Paragraph("Most Requested Services", styles["Heading2"]))
#             elements.append(Spacer(1, 6))
            
#             # Get services with request counts
#             from sqlalchemy import func
#             services_with_counts = []
#             try:
#                 services_with_counts = db.session.query(
#                     Service.name, 
#                     func.count(ServiceRequest.id).label('request_count')
#                 ).join(
#                     ServiceRequest, ServiceRequest.service_id == Service.id
#                 ).group_by(
#                     Service.id
#                 ).order_by(
#                     func.count(ServiceRequest.id).desc()
#                 ).limit(5).all()
#             except Exception as e:
#                 print(f"Error getting service counts: {str(e)}")
#                 # Fallback to a manual count
#                 service_count_dict = {}
#                 for req in ServiceRequest.query.all():
#                     service = Service.query.get(req.service_id)
#                     if service:
#                         service_name = service.name
#                         if service_name in service_count_dict:
#                             service_count_dict[service_name] += 1
#                         else:
#                             service_count_dict[service_name] = 1
                
#                 # Convert to sorted list of tuples
#                 services_with_counts = [(name, count) for name, count in 
#                                        sorted(service_count_dict.items(), key=lambda x: x[1], reverse=True)[:5]]
            
#             if services_with_counts:
#                 services_data = [["Service Name", "Number of Requests"]]
#                 for service in services_with_counts:
#                     services_data.append([service[0], str(service[1])])
                
#                 services_table = Table(services_data, colWidths=[300, 200])
#                 services_table.setStyle(TableStyle([
#                     ('BACKGROUND', (0, 0), (1, 0), colors.grey),
#                     ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
#                     ('ALIGN', (0, 0), (1, 0), 'CENTER'),
#                     ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
#                     ('FONTSIZE', (0, 0), (1, 0), 14),
#                     ('BOTTOMPADDING', (0, 0), (1, 0), 12),
#                     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                     ('GRID', (0, 0), (-1, -1), 1, colors.black)
#                 ]))
#                 elements.append(services_table)
#             else:
#                 elements.append(Paragraph("No service requests in the selected period", styles["Normal"]))
            
#             # Build the PDF
#             doc.build(elements)
            
#             print(f"PDF report generated successfully: {filename}")
#             return {
#                 "status": "success",
#                 "filename": filename,
#                 "filepath": filepath
#             }
#     except Exception as e:
#         import traceback
#         print(f"PDF Generation Error: {str(e)}")
#         print(traceback.format_exc())
#         return {
#             "status": "error",
#             "error": str(e)
#         }

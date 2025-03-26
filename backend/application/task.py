from celery import shared_task
from .models import User, ServiceProfessional, Service, ServiceRequest, Reviews, Role, BlockedUsers
import time
import datetime
import csv

#scheduled tasks
@shared_task(ignore_results = False, name = 'monthly_report')
def monthly_report():
    return "Monthly Reports Sent"

#User Triggered Tasks
@shared_task(ignore_results = False, name = 'download_csv_report')
def csv_report():
    time.sleep(6)
    users = User.query.all()
    service_rqst = ServiceRequest.query.all()   #ADMIN
    csv_file_name = f"service_report_{datetime.datetime.now().strftime('%f')}.csv" 
    #service_report_123456.csv
    with open(f'static/{csv_file_name}',"w", newline = "") as csvfile:
        sr_no = 1
        report_csv = csv.writer(csvfile, delimiter = ",")
        report_csv.writerow(["Sr. No.", "Service ID", "Customer ID", "Professional ID", "Date of Request", "Status", "Remarks","pin_code"])#header
        for sr in service_rqst:
            report_csv.writerow([sr_no, sr.service_id, sr.customer_id, sr.professional_id, sr.created_at, sr.status, sr.pin_code])
            sr_no += 1

    return csv_file_name

#Scheduled Tasks

@shared_task(ignore_results = False, name = 'daily_remainder')
def daily_remainder():
    return "Daily Remainder Sent"

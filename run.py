import schedule
import time
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from datetime import datetime
import logging
import configparser
import os

# Configuration Management
config = configparser.ConfigParser()
config.read('config.ini')

# Extract API details from configuration
sanity_api_url = config['API']['SANITY_API_URL']
api_key = config['API']['API_KEY']

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Helper Function for API Requests
def groq_request(query):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    payload = {
        'query': query
    }
    try:
        response = requests.post(sanity_api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"GROQ request error: {e}")
        raise

# Step 1: Trigger Workflow
def job():
    logger.info("Workflow triggered")
    try:
        # Step 2: Project Initialization
        project_details = fetch_project_details()
        validated_details = validate_project_data(project_details)

        # Step 3: Resource Allocation
        allocated_resources = allocate_resources(validated_details)
        update_project_management_system(allocated_resources)

        # Step 4: Supply Chain Management
        order_materials(validated_details)
        update_inventory()

        # Step 5: Safety Compliance
        safety_compliance = check_safety_compliance()
        if not safety_compliance['compliant']:
            send_safety_notifications(safety_compliance['issues'])

        # Step 6: Progress Tracking
        progress_data = track_progress()
        update_project_progress(progress_data)

        # Step 7: Financial Management
        update_financial_records()
        track_budget()

        # Step 8: Reporting
        report = generate_reports()
        send_reports(report)
        post_reports_to_cloud(report)
    except Exception as e:
        logger.error(f"Workflow error: {e}")
        error_handling(e)

# Define each step as a function
def fetch_project_details():
    query = '*[_type == "project"]{project_id, project_name, start_date, end_date}'
    response = groq_request(query)
    logger.info(f"Fetched project details: {response}")
    return response

def validate_project_data(data):
    if not data:
        raise ValueError("Project data is empty")
    # Example validation
    if 'project_id' not in data:
        raise ValueError("Missing project_id in project data")
    logger.info("Project data validated")
    return data

def allocate_resources(data):
    query = '*[_type == "resource"]{resource_id, resource_name, allocation_date}'
    response = groq_request(query)
    logger.info(f"Allocated resources: {response}")
    return response

def update_project_management_system(data):
    logger.info(f"Project management system updated with data: {data}")
    return {"status": "success"}

def order_materials(data):
    query = '*[_type == "material"]{material_id, material_name, order_date}'
    response = groq_request(query)
    logger.info(f"Ordered materials: {response}")
    return response

def update_inventory():
    logger.info("Inventory updated")
    return {"status": "success"}

def check_safety_compliance():
    query = '*[_type == "safety"]{compliant, issues}'
    response = groq_request(query)
    logger.info(f"Safety compliance check result: {response}")
    return response

def send_safety_notifications(issues):
    subject = "Safety Compliance Notification"
    body = f"Safety issues detected: {issues}"
    send_email(subject, body)

def track_progress():
    query = '*[_type == "progress"]{progress_id, progress_status, progress_date}'
    response = groq_request(query)
    logger.info(f"Tracked progress: {response}")
    return response

def update_project_progress(data):
    logger.info(f"Project progress updated with data: {data}")
    return {"status": "success"}

def update_financial_records():
    logger.info("Financial records updated")
    return {"status": "success"}

def track_budget():
    logger.info("Budget tracking completed")

def generate_reports():
    report_data = "Example Report Content"
    logger.info("Report generated")
    return report_data

def send_reports(report):
    subject = "Project Report"
    body = report
    send_email(subject, body)

def post_reports_to_cloud(report):
    logger.info("Report posted to cloud")

def send_email(subject, body):
    sender = config['Email']['SENDER_EMAIL']
    receiver = config['Email']['RECEIVER_EMAIL']
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(config['Email']['SMTP_SERVER'], config['Email']['SMTP_PORT'])
        server.starttls()
        server.login(sender, config['Email']['SENDER_PASSWORD'])
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
        logger.info(f"Email sent to {receiver}")
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise

def error_handling(error):
    log_error(error)
    notify_admin(error)

def log_error(error):
    logger.error(f"{datetime.now()}: {str(error)}")

def notify_admin(error):
    send_email("Workflow Error Alert", f"An error occurred: {error}")

def check_critical_events():
    logger.info("Critical events checked")

# Schedule the job
schedule.every().hour.do(job)

if __name__ == "__main__":
    logger.info("Starting the scheduled job...")
    job()  # Run the job immediately for testing purposes

    while True:
        schedule.run_pending()
        time.sleep(1)

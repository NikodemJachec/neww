import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser

def send_test_email():
    config = configparser.ConfigParser()
    config.read('config.ini')

    sender = config['Email']['SENDER_EMAIL']
    receiver = config['Email']['RECEIVER_EMAIL']
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Test Email"
    msg.attach(MIMEText("This is a test email.", 'plain'))

    try:
        server = smtplib.SMTP(config['Email']['SMTP_SERVER'], config['Email']['SMTP_PORT'])
        server.starttls()
        server.login(sender, config['Email']['SENDER_PASSWORD'])
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
        print(f"Email sent to {receiver}")
    except Exception as e:
        print(f"Error sending email: {e}")

send_test_email()


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email_notification(to, subject, message):
    """Sends an email notification to the user using SMTP server."""
    from_email = os.getenv('email')
    password = os.getenv('password')
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = subject
    body = message
    # Connect to the SMTP server and send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to, "Your registration process completed welcome to our ERP platform click here to login".format(login_link))
    server.quit()
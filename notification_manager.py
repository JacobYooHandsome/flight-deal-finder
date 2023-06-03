import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
load_dotenv()

class NotificationManager:
    def __init__(self):
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("EMAIL_PASS")
        self.emailObject = EmailMessage()
    
    def send_notification(self, subject, body):
        self.emailObject.clear()
        self.emailObject['From'] = self.email
        self.emailObject['To'] = self.email
        self.emailObject["Subject"] = subject
        self.emailObject.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email, self.password)
            smtp.sendmail(self.email, self.email, self.emailObject.as_string())
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

    def send_notification_self(self, subject, body, email_to=os.getenv("EMAIL")):
        self.emailObject.clear()
        self.emailObject['From'] = self.email
        self.emailObject['To'] = email_to
        self.emailObject["Subject"] = subject
        self.emailObject.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email, self.password)
            smtp.sendmail(self.email, email_to, self.emailObject.as_string())
    
    def send_notification_all(self, subject, body, all_emails):
        for email in all_emails:
            self.send_notification_self(subject, body, email)
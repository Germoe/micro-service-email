import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.environ.get('GMAIL_USER')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')

class Gmail():
    def __init__(self):
        pass

    def send(self, to, subject, body, body_type='html'):
        try:
            message = MIMEMultipart()
            text = MIMEText(body, body_type)
            message.attach(text)
            message['to'] = to
            message['subject'] = subject

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, to, message.as_string())
            server.close()

            print(f'Sent message to {to}')
            return True
        except Exception as error:
            print(f'An error occurred: {error}')
            return False
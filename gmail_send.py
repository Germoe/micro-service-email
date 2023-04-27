import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

GMAIL_USER = os.environ.get('GMAIL_USER')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')

def send_email(subject, body, to, body_type='html'):
    try:
        message = MIMEMultipart()
        text = MIMEText(body, body_type)
        message.attach(text)
        message['to'] = to
        message['subject'] = subject

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        print(f'Successfully logged in as {GMAIL_USER}',
              f' to send email to {to}', 
              f' with subject {subject}',
              f' and body {body}')
        server.sendmail(GMAIL_USER, to, message.as_string())
        server.close()

        print(f'Sent message to {to}')
        return True
    except Exception as error:
        print(f'An error occurred: {error}')
        return False
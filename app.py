import os
from flask import Flask, request
from gmail_send import send_email

from auth import require_api_key
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/send-email', methods=['POST'])
@require_api_key
def send_email_route():
    subject = request.form.get('subject')
    body = request.form.get('body')
    body_type = 'html'
    to = request.form.get('to')

    if not subject or not body or not to:
        return 'Missing required parameters', 400

    isSent = send_email(subject=subject, body=body, to=to, body_type=body_type)
    if not isSent:
        return 'Email failed to send', 500
    return 'Email sent successfully', 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
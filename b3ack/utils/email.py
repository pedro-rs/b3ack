"""Sending emails through an outlook account.
"""

import smtplib, ssl

# Initialise environment variables
import environ
import os

env = environ.Env()

class Email():
    port = 587  # For SSL
    smtp_server = "smtp.office365.com"
    context = ssl.create_default_context()

    def __init__(self):
        self.sender_email = env('NOREPLY_EMAIL')
        self.password = env('EMAIL_PASS')

    def send(self, receiver_email: str, subject: str, message: str):
        """Send an email.

        Args:
            receiver_email (str): Who the email should be sent to (format: <user>@<provider>.<domain>)
            subject (str): Email's subject
            message (str): Email's message
        """
        content = f'Subject: {subject}\n\n{message}'

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.ehlo()
            server.starttls(context=self.context)
            server.ehlo()
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, content)
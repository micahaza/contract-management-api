import smtplib
from email.mime.text import MIMEText
from threading import Thread
from flask import Flask, render_template


class MailSender(object):

    def __init__(self, app: Flask = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask = None):
        self.server_name = app.config['MAIL_SERVER']
        self.port = app.config['MAIL_PORT']
        self.username = app.config['MAIL_USERNAME']
        self.password = app.config['MAIL_PASSWORD']
        self.mail_enabled = app.config['MAIL_ENABLED']
        self.default_sender = app.config['MAIL_DEFAULT_SENDER']

    def build_message(self, recipient: str, subject: str, body: str, sender=None):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender or self.default_sender
        msg['To'] = recipient
        return msg

    def build_message_from_template(self, recipient: str, subject: str, template: str, sender=None, **kwargs):
        body = render_template('email/' + template + '.txt', **kwargs)
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender or self.default_sender
        msg['To'] = recipient
        return msg

    def send_message(self, msg: MIMEText):
        server = smtplib.SMTP_SSL(self.server_name, self.port)
        server.login(self.username, self.password)
        result = server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()
        return result

    def send_message_async(self, msg: MIMEText):
        thr = Thread(target=self.send_message, args=[msg])
        thr.start()
        return thr

import smtplib
from email.mime.text import MIMEText
from threading import Thread
from flask import Flask


class MailSender(object):

    def __init__(self, app: Flask = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask = None):
        self.server = app.config['MAIL_SERVER']
        self.port = app.config['MAIL_PORT']
        self.username = app.config['MAIL_USERNAME']
        self.password = app.config['MAIL_PASSWORD']
        self.mail_enabled = app.config['MAIL_ENABLED']

    def build_message(self, sender: str, recipient: str, subject: str, body: str):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient
        return msg

    def send_template(self, template: str):
        pass

    def send_message(self, msg: MIMEText):
        server = smtplib.SMTP_SSL(self.server, self.port)
        server.login(self.username, self.password)
        result = server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()
        return result

    def send_message_async(self, msg: MIMEText):
        thr = Thread(target=self.send_message, args=[msg])
        thr.start()
        return thr

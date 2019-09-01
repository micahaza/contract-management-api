import smtplib
from email.mime.text import MIMEText


class MailSender(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app=None):
        self.app = app

    def build_message(self, sender: str, recipient: str, subject: str, body: str):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient
        return msg

    def send_message(self, msg: MIMEText):
        server = smtplib.SMTP_SSL(self.app.config['MAIL_SERVER'], self.app.config['MAIL_PORT'])
        server.login(self.app.config['MAIL_USERNAME'], self.app.config['MAIL_PASSWORD'])
        result = server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()
        return result

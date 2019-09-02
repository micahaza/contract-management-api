from jcapi.extensions.mail import MailSender
from unittest import mock


@mock.patch('smtplib.SMTP_SSL', autospec=True)
def test_mail(mail_sender_mock, app):
    mail_sender_mock.return_value.login = mock.Mock(return_value={})
    mail_sender_mock.return_value.sendmail = mock.Mock(return_value={})
    ms = MailSender()
    ms.init_app(app)
    message = ms.build_message('info@blockspire.com', 'bajgli@gmail.com', 'Hi Bro', 'Simple body, eeee')
    ms.send_message(message)
    mail_sender_mock.return_value.login.assert_called_once_with(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    mail_sender_mock.return_value.sendmail.assert_called_once_with('info@blockspire.com', 'bajgli@gmail.com', message.as_string())


@mock.patch('smtplib.SMTP_SSL', autospec=True)
def test_async_mail(mail_sender_mock, app):
    mail_sender_mock.return_value.login = mock.Mock(return_value={})
    mail_sender_mock.return_value.sendmail = mock.Mock(return_value={})
    ms = MailSender()
    ms.init_app(app)
    message = ms.build_message('info@blockspire.com', 'bajgli@gmail.com', 'Hi Bro', 'Simple body, eeee')
    ms.send_message_async(message)
    mail_sender_mock.return_value.login.assert_called_once_with(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    mail_sender_mock.return_value.sendmail.assert_called_once_with('info@blockspire.com', 'bajgli@gmail.com', message.as_string())

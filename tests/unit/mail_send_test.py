from jcapi.extensions.mail import MailSender
from unittest import mock
from threading import Thread


@mock.patch('smtplib.SMTP_SSL', autospec=True)
def test_mail(mail_sender_mock, app):
    mail_sender_mock.return_value.login = mock.Mock(return_value={})
    mail_sender_mock.return_value.sendmail = mock.Mock(return_value={})
    ms = MailSender()
    ms.init_app(app)
    message = ms.build_message('bajgli@gmail.com', 'Hi Bro', 'Simple body, eeee')
    ms.send_message(message)
    mail_sender_mock.return_value.login.assert_called_once_with(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    mail_sender_mock.return_value.sendmail.assert_called_once_with(app.config['MAIL_DEFAULT_SENDER'], 'bajgli@gmail.com', message.as_string())


@mock.patch('smtplib.SMTP_SSL', autospec=True)
def test_async_mail(mail_sender_mock, app):
    mail_sender_mock.return_value.login = mock.Mock(return_value={})
    mail_sender_mock.return_value.sendmail = mock.Mock(return_value={})
    ms = MailSender()
    ms.init_app(app)
    message = ms.build_message('bajgli@gmail.com', 'Hi Bro', 'Simple body, eeee')
    ms.send_message_async(message)
    mail_sender_mock.return_value.login.assert_called_once_with(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    mail_sender_mock.return_value.sendmail.assert_called_once_with(app.config['MAIL_DEFAULT_SENDER'], 'bajgli@gmail.com', message.as_string())


@mock.patch('smtplib.SMTP_SSL', autospec=True)
def test_mail_from_template(mail_sender_mock, app):
    mail_sender_mock.return_value.login = mock.Mock(return_value={})
    mail_sender_mock.return_value.sendmail = mock.Mock(return_value={})
    ms = MailSender()
    ms.init_app(app)
    message = ms.build_message_from_template('bajgli@gmail.com',
                                             'Welcome To JustContracts.io',
                                             'welcome',
                                             name='Joe Doe',
                                             email_verification_link='http://yooooooo.com')
    ms.send_message(message)
    mail_sender_mock.return_value.login.assert_called_once_with(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    mail_sender_mock.return_value.sendmail.assert_called_once_with(app.config['MAIL_DEFAULT_SENDER'], 'bajgli@gmail.com', message.as_string())


@mock.patch('smtplib.SMTP_SSL', autospec=True)
def test_non_blocking_mail_send(mail_sender_mock, app):
    mail_sender_mock.return_value.login = mock.Mock(return_value={})
    mail_sender_mock.return_value.sendmail = mock.Mock(return_value={})
    ms = MailSender()
    ms.init_app(app)
    message = ms.build_message_from_template('bajgli@gmail.com',
                                             'Welcome To JustContracts.io',
                                             'welcome',
                                             name='Joe Doe',
                                             email_verification_link='http://yooooooo.com')
    result = ms.send_message_async(message)
    assert isinstance(result, Thread)
    mail_sender_mock.return_value.login.assert_called_once_with(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    mail_sender_mock.return_value.sendmail.assert_called_once_with(app.config['MAIL_DEFAULT_SENDER'], 'bajgli@gmail.com', message.as_string())


def test_mail_send(app):
    # has to be mocked
    from jcapi import mail
    message = mail.build_message('info@blockspire.com', 'bajgli@gmail.com', 'Hi Bro', 'Simple body, eeee')
    print(message)

    # mail.send_message(message)

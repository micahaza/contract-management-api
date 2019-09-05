from jcapi.models import User
import pytest
import json
from unittest import mock

wrong_registration_data = [
    (dict(username='as', email='bajgli+1@gmail.com', password='asdfasdf', first_name=''), 400),
    (dict(username='asdf', email='', password='asdfasdf', first_name='joe', last_name='Booo'), 400),
    (dict(username='aasdasds', email='bajgli+2@gmail.com', password='', first_name='joe', last_name='Booo'), 400),
    (dict(username='', email='', password='', first_name='joe', last_name='Booo'), 400),
    (dict(username='äđ¶', email='hola at booo dot com', password='', first_name='joe', last_name='Booo'), 400)
]

correct_registration_data = [
    (dict(username='asasdf', email='bajgli+3@gmail.com', password='supersecret', first_name='Super', last_name='Man'), 200),
    (dict(username='goodusername', email='bajgli+4@gmail.com', password='asdfasdflong', first_name='Super', last_name='Man'), 200),
    (dict(username='badaboooo', email='bajgli+5@gmail.com', password='goodenough', first_name='Super', last_name='Man'), 200)
]


@pytest.mark.parametrize("test_input, expected_output", correct_registration_data)
@mock.patch('smtplib.SMTP_SSL', autospec=True)
def test_user_can_register(mail_sender_mock, test_client, test_input, expected_output):
    mail_sender_mock.return_value.login = mock.Mock(return_value={})
    mail_sender_mock.return_value.sendmail = mock.Mock(return_value={})

    response = test_client.post('/api/v1/registration/', json=test_input)
    assert response.status_code == expected_output
    assert 'token' in json.loads(response.data)
    new_user = User.query.filter_by(username=test_input['username']).first()
    assert new_user.email == test_input['email']
    assert new_user.password_hash is not None


@pytest.mark.parametrize("test_input, expected_output", wrong_registration_data)
def test_missing_data(test_client, test_input, expected_output):
    response = test_client.post('/api/v1/registration/', json=test_input)
    assert response.status_code == expected_output


def test_user_can_not_register_twice(test_client):
    reg_data = dict(username='goodusername2', email='gooduser2@gmail.com', password='asdfasdflong2', first_name='Super', last_name='Man')
    response = test_client.post('/api/v1/registration/', json=reg_data)
    assert response.status_code == 200
    response = test_client.post('/api/v1/registration/', json=reg_data)
    assert response.status_code == 409


def test_email_validation(test_client):
    reg_data = dict(username='tqtqtq', email='tqtqtq@gmail.com', password='tqtqtqtqtqtq', first_name='Super', last_name='Man')
    response = test_client.post('/api/v1/registration/', json=reg_data)
    assert response.status_code == 200
    email_validation_token = json.loads(response.data)

    response = test_client.post('/api/v1/registration/email-validation/', json=email_validation_token)
    assert response.status_code == 200
    resp_data = json.loads(response.data)
    assert 'message' in resp_data
    user = User.query.filter_by(email=reg_data['email']).first()
    assert user.active is True
    assert user.email_verified is True

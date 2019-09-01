from jcapi.models import User
import pytest
import json

wrong_registration_data = [
    (dict(username='as', email='asdf@asdf.hu', password='asdfasdf'), 400),
    (dict(username='asdf', email='', password='asdfasdf'), 400),
    (dict(username='aasdasds', email='asdf@asdf.hu', password=''), 400),
    (dict(username='', email='', password=''), 400),
    (dict(username='äđ¶', email='hola at booo dot com', password=''), 400)
]

correct_registration_data = [
    (dict(username='asasdf', email='booge@gmail.com', password='supersecret'), 200),
    (dict(username='goodusername', email='gooduser@gmail.com', password='asdfasdflong'), 200),
    (dict(username='badaboooo', email='badaboooo@flask.com', password='goodenough'), 200)
]


@pytest.mark.parametrize("test_input, expected_output", correct_registration_data)
def test_user_can_register(test_client, test_input, expected_output):
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
    reg_data = dict(username='goodusername2', email='gooduser2@gmail.com', password='asdfasdflong2')
    response = test_client.post('/api/v1/registration/', json=reg_data)
    assert response.status_code == 200
    response = test_client.post('/api/v1/registration/', json=reg_data)
    assert response.status_code == 409


def test_email_validation(test_client):
    reg_data = dict(username='tqtqtq', email='tqtqtq@gmail.com', password='tqtqtqtqtqtq')
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

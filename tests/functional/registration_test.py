from jcapi.models import User
import pytest


wrong_registration_data = [
    (dict(username='as', email='asdf@asdf.hu', password='asdfasdf'), 400),
    (dict(username='asdf', email='', password='asdfasdf'), 400),
    (dict(username='aasdasds', email='asdf@asdf.hu', password=''), 400),
    (dict(username='', email='', password=''), 400),
    (dict(username='äđ¶', email='hola at booo dot com', password=''), 400)
]

correct_registration_data = [
    (dict(username='asasdf', email='booge@gmail.com', password='supersecret'), 204),
    (dict(username='goodusername', email='gooduser@gmail.com', password='asdfasdflong'), 204),
    (dict(username='badaboooo', email='badaboooo@flask.com', password='goodenough'), 204)
]


@pytest.mark.parametrize("test_input, expected_output", correct_registration_data)
def test_user_can_register(test_client, test_input, expected_output):
    response = test_client.post('/api/v1/registration/', json=test_input)
    assert response.status_code == expected_output
    new_user = User.query.filter_by(username=test_input['username']).first()
    assert new_user.email == test_input['email']
    assert new_user.password_hash is not None


@pytest.mark.parametrize("test_input, expected_output", wrong_registration_data)
def test_missing_data(test_client, test_input, expected_output):
    response = test_client.post('/api/v1/registration/', json=test_input, follow_redirects=True)
    assert response.status_code == expected_output


def test_user_can_not_register_twice(test_client):
    reg_data = dict(username='goodusername2', email='gooduser2@gmail.com', password='asdfasdflong2')
    response = test_client.post('/api/v1/registration/', json=reg_data)
    assert response.status_code == 204
    response = test_client.post('/api/v1/registration/', json=reg_data)
    assert response.status_code == 409

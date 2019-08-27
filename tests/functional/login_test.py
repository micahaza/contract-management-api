import pytest
import json

wrong_login_data = [
    (dict(username='deezent_not_exist', password='deezentpass'), 404),
    (dict(username='deezent', password='deezent_wrong_pass'), 500),
    (dict(username='trickyUserName', password='omg_my_pass'), 404),
]


@pytest.mark.parametrize("test_input, expected_output", wrong_login_data)
def test_wrong_user_credentials(test_client, user, test_input, expected_output):
    response = test_client.post('/auth/login/', json=test_input)
    assert response.status_code == expected_output


def test_user_can_login(test_client, user):
    test_input = dict(username=user.username, password='deezentpass')
    response = test_client.post('/auth/login/', json=test_input)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'access_token' in response_data


def test_jwt_protected(test_client, header_with_token):
    response = test_client.get('/auth/logout/', headers=header_with_token)
    assert response.status_code == 200


def test_jwt_protected_endpoint_fails_without_token(test_client):
    response = test_client.get('/auth/logout/')
    response_data = json.loads(response.data)
    assert response_data['msg'] == 'Missing Authorization Header'
    assert response.status_code == 401

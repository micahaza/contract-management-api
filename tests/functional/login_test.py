import pytest
import json

wrong_login_data = [
    (dict(username='deezent_not_exist', password='deezentpass'), 403),
    (dict(username='deezent', password='deezent_wrong_pass'), 403),
    (dict(username='trickyUserName', password='omg_my_pass'), 403),
]


@pytest.mark.parametrize("test_input, expected_output", wrong_login_data)
def test_wrong_user_credentials(test_client, user, test_input, expected_output):
    response = test_client.post('/api/v1/auth/login/', json=test_input)
    assert response.status_code == expected_output


def test_user_can_login(test_client, valid_user):
    test_input = dict(username=valid_user.username, password='deezentpass')
    response = test_client.post('/api/v1/auth/login/', json=test_input)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'access_token' in response_data

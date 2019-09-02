import json


def test_can_get_password_reset_token(test_client, valid_user):
    # requesting the password reset token
    payload = {'email': valid_user.email}
    response = test_client.post('/api/v1/auth/password-reset-request/', json=payload)
    data = json.loads(response.data)
    assert 'token' in data
    assert response.status_code == 200
    print(valid_user.password_hash)

    # setting new password
    payload = {'token': data['token'], 'new_password': 'password_has_been_changed'}
    response = test_client.post('/api/v1/auth/password-reset/', json=payload)
    assert response.status_code == 200

    # user can login now
    test_input = dict(username=valid_user.username, password='password_has_been_changed')
    response = test_client.post('/api/v1/auth/login/', json=test_input)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'access_token' in response_data

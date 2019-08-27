import json


def test_application_loads(test_client):
    response = test_client.get('/api/v1/')
    assert response.status_code == 200


def test_application_returns_json(test_client):
    response = test_client.get('/api/v1/')
    assert response.headers['Content-Type'] == 'application/json'


def test_jwt_protected_endpoint_fails_without_token(test_client):
    response = test_client.get('/api/v1/ping/')
    response_data = json.loads(response.data)
    assert response_data['msg'] == 'Missing Authorization Header'
    assert response.status_code == 401


def test_jwt_protected_ok(test_client, header_with_token):
    response = test_client.get('/api/v1/ping/', headers=header_with_token)
    response_data = json.loads(response.data)
    assert response_data['msg'] == 'pong'
    assert response.status_code == 200

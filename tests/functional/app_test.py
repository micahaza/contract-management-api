def test_application_loads(test_client):
    response = test_client.get('/')
    assert response.status_code == 200


def test_application_returns_json(test_client):
    response = test_client.get('/')
    assert response.headers['Content-Type'] == 'application/json'

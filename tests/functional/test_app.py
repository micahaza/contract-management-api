def test_application_loads(test_client):
    response = test_client.get('/')
    print(response)
    assert response.status_code == 200

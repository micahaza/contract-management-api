def test_application_loads(test_client):
    response = test_client.get('/registration/')
    print(response)
    assert response.status_code == 200

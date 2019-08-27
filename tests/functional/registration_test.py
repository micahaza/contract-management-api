def test_page_loads(test_client):
    response = test_client.get('/registration/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration" in response.data


def test_user_can_register(test_client):
    reg_data = dict(username='asdf', email='adsf@asdf.hu', password='asdf')
    response = test_client.post('/registration/', json=reg_data, follow_redirects=True)
    assert response.status_code == 200

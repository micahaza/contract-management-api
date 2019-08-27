from jcapi.models import User


def test_user_can_register(test_client):
    reg_data = dict(username='asdf', email='asdf@asdf.hu', password='asdf')
    response = test_client.post('/registration/', json=reg_data, follow_redirects=True)
    assert response.status_code == 204
    new_user = User.query.filter_by(username='asdf').first()
    assert new_user.email == 'asdf@asdf.hu'
    assert new_user.password_hash is not None

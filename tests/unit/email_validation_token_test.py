from jcapi.extensions.token import TokenManager


def test_token_generation(app, user):
    tm = TokenManager(app)
    token = tm.get_token({'user_id': user.id, 'email': user.email})
    assert token is not None
    assert type(token) is str

    deserialized = tm.confirm_token(token)
    assert deserialized['user_id'] == user.id
    assert deserialized['email'] == user.email

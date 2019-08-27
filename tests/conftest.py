import pytest
from jcapi import create_app, db


@pytest.fixture(scope='module')
def app():
    app = create_app('testing.cfg')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def test_client(app):
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield testing_client  # this is where the testing happens!
    ctx.pop()

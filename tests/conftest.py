import pytest
from jcapi import create_app, db
from jcapi.models import User, Contract
from flask_jwt_extended import create_access_token


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


@pytest.fixture(scope='module')
def user(app):
    user = User('deezent', 'deezent@gmail.com', 'deezentpass')
    db.session.add(user)
    db.session.commit()
    yield user


@pytest.fixture(scope='module')
def header_with_token(user):
    access_token = create_access_token(user.username)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    yield headers


@pytest.fixture(scope='module')
def contract_text():
    with open('./tests/nda-contract.txt') as file:
        data = file.readlines()
    return data[0]


@pytest.fixture(scope='module')
def contract(contract_text, user):
    contract = Contract()
    contract.name = 'Non Disclosure Agreement'
    contract.description = 'trust each other, just for fun'
    contract.legal_text = contract_text
    contract.effective_date = '2019-09-01'
    contract.expiration_date = '2019-12-01'
    contract.currency = 'EUR'
    contract.status = 'DRAFT'
    contract.owner_id = user.id
    db.session.add(contract)
    db.session.commit()
    yield contract

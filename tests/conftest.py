import pytest
from jcapi import create_app, db
from jcapi.models import User, Contract, TemplateTag
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
def valid_user(app):
    user = User('deezent_valid', 'deezent_valid@gmail.com', 'deezentpass')
    user.active = True
    user.email_verified = True
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
    contract.version = 1
    contract.name = 'Non Disclosure Agreement'
    contract.description = 'trust each other, just for fun'
    contract.legal_text = contract_text
    contract.effective_date = '2019-09-01'
    contract.expiration_date = '2019-12-01'
    contract.currency = 'EUR'
    contract.status = 'DRAFT'
    contract.owner_id = user.id

    party1 = User('deezent1', 'deezent1@gmail.com', 'deezentpass1')
    party2 = User('deezent2', 'deezent2@gmail.com', 'deezentpass2')
    party3 = User('deezent3', 'deezent3@gmail.com', 'deezentpass3')
    contract.parties.extend([party1, party2, party3])

    tt1 = TemplateTag('key1', 'value1')
    tt2 = TemplateTag('key3', 'value3')
    tt3 = TemplateTag('key1', 'value3')
    contract.template_tags.append(tt1)
    contract.template_tags.append(tt2)
    contract.template_tags.append(tt3)

    db.session.add(contract)
    db.session.commit()
    yield contract

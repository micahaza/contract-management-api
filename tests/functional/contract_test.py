from datetime import datetime
from jcapi.models import Contract
import json

contract_data = {
    'name': 'Non Disclosure Agreement',
    'description': 'We trust each other, just for fun',
    'legal_text': '',
    'effective_date': datetime.today().strftime('%Y-%m-%d'),
    'expiration_date': datetime.today().strftime('%Y-%m-%d'),
    'currency': 'EUR',
    'status': 'DRAFT'
}


def test_can_create_contract(test_client, header_with_token, contract_text):
    contract_data['legal_text'] = contract_text
    response = test_client.post('/api/v1/contract/', json=contract_data, headers=header_with_token)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    contract = Contract.query.get(int(response_data['id']))
    assert contract is not None
    assert contract.currency == contract_data['currency']
    assert contract.status == contract_data['status']
    assert contract.name == contract_data['name']
    assert contract.description == contract_data['description']


def test_get_contract(test_client, header_with_token, contract):
    response = test_client.get('/api/v1/contract/' + str(contract.id), headers=header_with_token)
    response_data = json.loads(response.data)
    assert response.status_code == 200
    assert response_data['description'] == contract.description
    assert response_data['status'] == contract.status
    assert response_data['currency'] == contract.currency
    assert response_data['legal_text'] == contract.legal_text
    assert len(response_data['parties']) == 3


def test_get_non_existent_contract(test_client, header_with_token):
    response = test_client.get('/api/v1/contract/92837423', headers=header_with_token)
    response_data = json.loads(response.data)
    assert response.status_code == 404
    assert response_data['msg'] == 'Contract not found'

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import Schema, validate, fields
from jcapi.models import Contract
from jcapi import db


contract = Blueprint('contract', __name__)


@jwt_required
@contract.route('/', methods=['POST'])
def create_contract():
    rv = request.get_json()
    errors = CreateContractSchema().validate(rv)
    if errors:
        return jsonify({}), 400
    contract = Contract()
    contract.name = rv['name']
    contract.description = rv['description']
    contract.legal_text = rv['legal_text']
    contract.effective_date = rv['effective_date']
    contract.expiration_date = rv['expiration_date']
    contract.currency = rv['currency']
    contract.status = rv['status']
    contract.owner_id = 1
    db.session.add(contract)
    db.session.commit()

    return jsonify(contract.to_dict()), 200


class CreateContractSchema(Schema):
    name = fields.String(validate=validate.Length(min=3, max=128), required=True)
    description = fields.String()
    legal_text = fields.String(required=True)
    effective_date = fields.Date()
    expiration_date = fields.Date()
    currency = fields.String(validate=validate.Length(min=3, max=3))
    status = fields.String(validate=validate.Length(min=3, max=32))


class UpdateContractSchema(Schema):
    version = fields.Integer(required=False)
    name = fields.String(validate=validate.Length(min=3, max=128), required=True)
    description = fields.String()
    legal_text = fields.String(required=True)
    effective_date = fields.Date()
    expiration_date = fields.Date()
    currency = fields.String(validate=validate.Length(min=3, max=3))
    status = fields.String(validate=validate.Length(min=3, max=32))

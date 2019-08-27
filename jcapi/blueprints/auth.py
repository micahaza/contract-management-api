from flask import Blueprint, request, jsonify
from jcapi import bcrypt
from jcapi.models import User
from marshmallow import Schema, validate, fields
from flask_jwt_extended import create_access_token


auth = Blueprint('auth', __name__)


@auth.route('/login/', methods=['POST'])
def user_login():
    req_data = request.get_json()
    errors = LoginSchema().validate(req_data)
    if errors:
        return jsonify({}), 400
    username = req_data['username']
    password = req_data['password']
    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify(dict(error='User not exists')), 404
    elif bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'error': 'wrong password'}), 500


class LoginSchema(Schema):
    username = fields.String(validate=validate.Length(min=3, max=25), required=True)
    password = fields.String(validate=validate.Length(min=8, max=100), required=True)

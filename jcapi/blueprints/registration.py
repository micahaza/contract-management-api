from flask import Blueprint, request, jsonify
from jcapi.models import User
from jcapi import db, token_manager
from marshmallow import Schema, fields, validate


registration = Blueprint('registration', __name__)


@registration.route('/', methods=['POST'])
def register():
    req_data = request.get_json()
    errors = UserSchema().validate(req_data)
    if errors:
        return jsonify({}), 400
    username = req_data['username']
    email = req_data['email']
    password = req_data['password']
    u_exists = User.query.filter_by(username=username).first()
    if u_exists is None:
        u = User(username, email, password)
        db.session.add(u)
        db.session.commit()
        token = token_manager.get_email_validation_token({'user_id': u.id, 'email': u.email})
    else:
        return jsonify(dict(error='User already registered')), 409
    return jsonify({'token': token}), 200


@registration.route('/email-validation/', methods=['POST'])
def validate_registration_token():
    req_data = request.get_json()
    u_data = token_manager.confirm_token(req_data['token'])
    user = User.query.get(int(u_data['user_id']))
    if user is not None:
        user.active = True
        user.email_verified = True
        db.session.add(user)
        db.session.commit()
    return jsonify({'message': 'ok'}), 200


class UserSchema(Schema):
    username = fields.String(validate=validate.Length(min=3, max=25), required=True)
    email = fields.String(validate=validate.Email(), required=True)
    password = fields.String(validate=validate.Length(min=8, max=100), required=True)

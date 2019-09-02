from flask import Blueprint, request, jsonify
from jcapi.models import User
from marshmallow import Schema, validate, fields
from flask_jwt_extended import create_access_token
from jcapi import token_manager, bcrypt, db

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
        return jsonify(dict(error='User not exists')), 403
    elif user.active is False:
        return jsonify(dict(error='User is not active')), 403
    elif user.email_verified is False:
        return jsonify(dict(error='User email is not verified')), 403
    elif bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'error': 'wrong password'}), 500


@auth.route('/password-reset-request/', methods=['POST'])
def password_reset_request():
    req_data = request.get_json()
    user = User.query.filter_by(email=req_data['email']).first()
    if user is not None:
        token = token_manager.get_token(req_data)
        return jsonify({'token': token}), 200
    else:
        return jsonify(dict(error='User not exists')), 403


@auth.route('/password-reset/', methods=['POST'])
def password_reset():
    req_data = request.get_json()
    decoded_data = token_manager.confirm_token(req_data['token'])
    if 'email' in decoded_data and 'new_password' in req_data:
        user = User.query.filter_by(email=decoded_data['email']).first()
        if user is not None:
            user.password_hash = bcrypt.generate_password_hash(req_data['new_password']).decode('utf-8')
            db.session.add(user)
            db.session.commit()
            return jsonify(dict(message='Password has been changed')), 200
    else:
        return jsonify(dict(error='Something went wrong')), 500


class LoginSchema(Schema):
    username = fields.String(validate=validate.Length(min=3, max=25), required=True)
    password = fields.String(validate=validate.Length(min=8, max=100), required=True)

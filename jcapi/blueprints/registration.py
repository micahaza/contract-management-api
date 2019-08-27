from flask import Blueprint, request, jsonify
from jcapi.models import User
from jcapi import db

registration = Blueprint('registration', __name__)


@registration.route('/', methods=['POST'])
def register():
    req_data = request.get_json()
    username = req_data['username']
    email = req_data['email']
    password = req_data['password']
    u_exists = User.query.filter_by(username=username).first()
    if u_exists is None:
        u = User(username, email, password)
        db.session.add(u)
        db.session.commit()
    return jsonify({}), 204

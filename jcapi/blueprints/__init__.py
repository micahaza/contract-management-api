from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required


home = Blueprint('home', __name__)


@home.route('/')
def default():
    return jsonify({}), 200


@home.route('/ping/')
@jwt_required
def ping():
    return jsonify({'msg': 'pong'})

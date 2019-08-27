from flask import Blueprint, jsonify


home = Blueprint('home', __name__)


@home.route('/')
def default():
    return jsonify({}), 200

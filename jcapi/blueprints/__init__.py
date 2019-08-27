from flask import Blueprint


registration = Blueprint('registration', __name__)


@registration.route('/')
def register():
    return 'registration'

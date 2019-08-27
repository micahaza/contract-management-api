from flask import Blueprint


registration = Blueprint('registration', __name__)
home = Blueprint('home', __name__)


@registration.route('/')
def register():
    return 'registration'


@home.route('/')
def default():
    return 'home'

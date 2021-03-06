from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from jcapi.extensions.mail import MailSender
from jcapi.extensions.token import TokenManager

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = MailSender()
token_manager = TokenManager()


def create_app(config_filename: str = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    token_manager.init_app(app)


def register_blueprints(app: Flask):
    from jcapi.blueprints import home as home_blueprint
    from jcapi.blueprints.auth import auth as auth_blueprint
    from jcapi.blueprints.registration import registration as registration_blueprint
    from jcapi.blueprints.contract import contract as contract_blueprint

    app.register_blueprint(home_blueprint, url_prefix='/api/v1')
    app.register_blueprint(registration_blueprint, url_prefix='/api/v1/registration')
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')
    app.register_blueprint(contract_blueprint, url_prefix='/api/v1/contract')

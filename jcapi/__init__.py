from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)


def register_blueprints(app):
    from jcapi.blueprints import home as home_blueprint
    from jcapi.blueprints.auth import auth as auth_blueprint
    from jcapi.blueprints.registration import registration as registration_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(registration_blueprint, url_prefix='/registration')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')


from jcapi.models import User # noqa

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


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


def register_blueprints(app):
    from jcapi.blueprints import home as home_blueprint
    from jcapi.blueprints.registration import registration as registration_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(registration_blueprint, url_prefix='/registration')


from jcapi.models import User # noqa

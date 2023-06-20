import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

# with app.app_context():
#     from . import routes
#     db.create_all()


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    if app.debug:
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.ProductionConfig')

    # This import is necessary so that models
    # are detected by Flask-Migrate
    from . import models

    db.init_app(app)
    migrate.init_app(app, db)

    return app

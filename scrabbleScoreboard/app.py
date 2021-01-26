from flask import Flask

from scrabbleScoreboard import api
from scrabbleScoreboard import auth
from scrabbleScoreboard.extensions import db, migrate, jwt, swagger
from scrabbleScoreboard.manage import cli


def create_app(testing=False):
    """Application factory, used to create application."""
    app = Flask("scrabbleScoreboard")
    app.config.from_object("scrabbleScoreboard.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    register_blueprints(app)
    register_commands(app)

    return app

def configure_extensions(app):
    """Initialize application extensions."""
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

def register_blueprints(app):
    """Register all blueprints for applications."""
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(auth.views.blueprint)

def register_commands(app):
    """Register custom commands for application."""
    app.cli.add_command(cli)
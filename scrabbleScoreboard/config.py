import os


ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_ERROR_MESSAGE_KEY = os.getenv("JWT_ERROR_MESSAGE_KEY")
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

FLASK_ADMIN_SWATCH = 'sandstone'


SWAGGER = {
    "title": "Scrabble Scoreboard API",
    "uiversion": 3,
    "specs_route": "/docs",
    "openapi": "3.0.3",
    "specs": [{
        "endpoint": 'apispec',
        "route": '/apispec.json',
        "rule_filter": lambda rule: True,
        "model_filter": lambda tag: True,
    }]
}

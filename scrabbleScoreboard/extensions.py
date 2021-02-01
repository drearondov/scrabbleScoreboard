"""Extensions registry

All extensions here are used as singletons and initialized in an application factory
"""

from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flasgger import Swagger


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Scrabble Scoreboard",
        "description": "An API to record store data from Scrabble games",
        "version": "0.1.0-alpha",
    },
    "schemes": ["http", "https"],
}


db = SQLAlchemy(metadata=metadata)
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()
swagger = Swagger(template=swagger_template)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

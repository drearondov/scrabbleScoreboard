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
from flask_admin import Admin
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from scrabbleScoreboard.utils.swagger import swagger_template


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


db = SQLAlchemy(metadata=metadata)
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()
swagger = Swagger(template=swagger_template)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
manager = Admin(name='Scrabble Scoreboard', template_mode='bootstrap3')
login_manager = LoginManager()
bootstrap = Bootstrap()

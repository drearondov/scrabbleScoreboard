from enum import unique
from sqlalchemy.ext.hybrid import hybrid_property

from scrabbleScoreboard.extensions import db, pwd_context


class Admin(db.Model):
    """Model for administrator"""

    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self) -> str:
        return f"<Admin {self.admin_name}>"

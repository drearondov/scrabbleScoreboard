from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin

from scrabbleScoreboard.extensions import login, db, pwd_context


class Admin(UserMixin, db.Model):
    """Model for administrator"""

    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean(name="is_active"), default=True)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def verify_password(self, password):
        return pwd_context.verify(password, self._password)

    @login.user_loader
    def load_user(id):
        return Admin.query.get(int(id))

    def __repr__(self) -> str:
        return f"<Admin {self.admin_name}>"

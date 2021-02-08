from flask import redirect, url_for, request
from flask.helpers import flash
from flask_admin.base import expose, AdminIndexView
from flask_admin.form import SecureForm
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_login.utils import login_user, logout_user

from scrabbleScoreboard.models import Language, Word, Game, Player, Play, Admin
from scrabbleScoreboard.forms import LoginForm
from scrabbleScoreboard.extensions import manager, db


class ProtectedModelView(ModelView):
    """
    Custom model view to add support for authentication in admin side.
    """

    form_base_class = SecureForm

    def is_accessible(self):
        return current_user.is_authenticated


class NewAdminIndexView(AdminIndexView):
    """
    Custom model to handle login from the admin side.
    """

    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for(".login_view"))
        return super(NewAdminIndexView, self).index()

    @expose("/login", methods=("GET", "POST"))
    def login_view(self):
        if current_user.is_authenticated:
            return super(NewAdminIndexView, self).index()

        form = LoginForm(request.form)

        if form.validate_on_submit():
            admin = Admin.query.filter_by(admin_name=form.admin_name.data).first()

            if admin is None or not admin.verify_password(form.password.data):
                flash("Invalid administrator or password")
                return redirect(url_for(".login_view"))

            login_user(admin, remember=form.remember_me.data)
            return super(NewAdminIndexView, self).index()

        self._template_args["form"] = form
        return super(NewAdminIndexView, self).index()

    @expose("/logout")
    def logout_view(self):
        logout_user()
        return redirect(url_for(".index"))


manager.add_view(ProtectedModelView(Language, db.session))
manager.add_view(ProtectedModelView(Word, db.session))
manager.add_view(ProtectedModelView(Game, db.session))
manager.add_view(ProtectedModelView(Player, db.session))
manager.add_view(ProtectedModelView(Play, db.session))

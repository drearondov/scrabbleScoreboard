from flask import render_template

from scrabbleScoreboard.forms import LoginForm


def login():
    login_form = LoginForm()
    return render_template("index.j2", form=login_form)

from flask.helpers import url_for
from app.forms import LoginForm
from flask import render_template, flash, redirect

from app import app


@app.route('/')
@app.route('/scoreboard')
def scoreboard():
    player = {'name': 'Donis'}
    return render_template('index.j2', title='Scrabble', player=player)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for {form.player.data}, remember_me = {form.remember_me.data}')
        return redirect(url_for('soreboard'))
    return render_template('login.j2', title='Sign in', form=form)

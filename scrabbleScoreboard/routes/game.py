from flask import render_template, redirect, request
from flask.helpers import url_for

from scrabbleScoreboard.forms import NewPlayForm
from scrabbleScoreboard.models import Game, Play


def game():
    play_form = NewPlayForm()
    current_game = request.cookies.get("game_id")

    # Form processing
    if play_form.validate_on_submit():
        Play.form_create_play(
            play_form.word.data,
            play_form.language.data,
            Game.query.get(current_game),
            play_form.player.data,
            play_form.score.data,
            play_form.turn.data
        )
        return redirect(url_for(".game"))


    return render_template("game.j2", form=play_form, game=current_game)

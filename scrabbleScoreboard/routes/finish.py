from flask import redirect
from flask.helpers import url_for

from scrabbleScoreboard.models import Game


def finish():
    current_game = Game.query.get(1)

    current_game.set_winner()
    current_game.is_active = False
    current_game.save()

    return redirect(url_for(".home"))
from flask import render_template, redirect, make_response
from flask.helpers import url_for

from scrabbleScoreboard.extensions import db
from scrabbleScoreboard.forms import NewGameForm
from scrabbleScoreboard.models import Player, Game, GametypeEnum, game


def home():
    game_form = NewGameForm()

    if game_form.validate_on_submit():

        gametype = {"normal": GametypeEnum.normal, "timed": GametypeEnum.timed}

        game_players = []

        form_players = [
            game_form.player_1.data,
            game_form.player_2.data,
            game_form.player_3.data,
            game_form.player_4.data,
        ]

        for player in form_players:
            if player is not None:
                game_players.append(Player.get_or_create(name=player))

        new_game = Game(
            gametype=gametype[game_form.gametype.data],
            players=game_players,
            is_active=True,
        )

        db.session.add(new_game)
        db.session.commit()

        response = make_response(redirect(url_for(".game")))
        response.set_cookie("game_id", new_game.id)

        return response

    return render_template("menu.j2", form=game_form)

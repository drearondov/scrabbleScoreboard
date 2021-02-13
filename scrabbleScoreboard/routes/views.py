from flask import Blueprint, render_template

from scrabbleScoreboard.forms import LoginForm, NewGameForm, NewPlayForm
from scrabbleScoreboard.models import Player, Game


blueprint = Blueprint('main', __name__)


@blueprint.route('/', methods=["GET", "POST"])
@blueprint.route('/login', methods=["GET", "POST"])
def index():
    login_form = LoginForm()
    return render_template('index.j2', form=login_form)


@blueprint.route('/home', methods=["GET", "POST"])
def home():
    new_game_form = NewGameForm()
    return render_template('menu.j2', form=new_game_form)


@blueprint.route('/game', methods=["GET", "POST"])
def game():
    new_play_form = NewPlayForm()
    game_players = Player.query.filter_by(games=Game.query.filter_by(is_active=True).first()).all()
    return render_template('game.j2', form=new_play_form, game_players=game_players)

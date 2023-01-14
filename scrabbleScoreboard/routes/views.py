from flask import Blueprint

from scrabbleScoreboard.routes.finish import finish
from scrabbleScoreboard.routes.game import game
from scrabbleScoreboard.routes.home import home
from scrabbleScoreboard.routes.login import login


blueprint = Blueprint("main", __name__)


blueprint.add_url_rule("/", view_func=login, methods=["GET", "POST"])
blueprint.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
blueprint.add_url_rule("/home", view_func=home, methods=["GET", "POST"])
blueprint.add_url_rule("/game", view_func=game, methods=["GET", "POST"])
blueprint.add_url_rule("/finish", view_func=finish, methods=["GET", "POST"])

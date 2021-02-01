from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from http import HTTPStatus

from scrabbleScoreboard.api.resources import (
    WordListResource,
    WordLanguageListResource,
    GameListResource,
    GameResource,
    PlayResource,
    PlayListResource,
    PlayerResource,
    PlayerListResource,
    PlaysGameListResource,
    PlaysPlayerListResource,
)


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(WordListResource, "/words", endpoint="words")
api.add_resource(
    WordLanguageListResource,
    "/words/languages/<string:language_name>",
    endpoint="words_in_language",
)

api.add_resource(GameListResource, "/games", endpoint="games")
api.add_resource(GameResource, "/games/<int:game_id>", endpoint="game_by_id")
api.add_resource(
    PlaysGameListResource, "/games/<int:game_id>/plays", endpoint="plays_from_game"
)

api.add_resource(PlayerListResource, "/players", endpoint="players")
api.add_resource(PlayerResource, "/players/<int:player_id>", endpoint="player_by_id")
api.add_resource(
    PlaysPlayerListResource,
    "/players/<int:player_id>/plays",
    endpoint="plays_by_player",
)

api.add_resource(PlayListResource, "/plays", endpoint="plays")
api.add_resource(PlayResource, "/plays/<int:play_id>", endpoint="play_by_id")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), HTTPStatus.BAD_REQUEST

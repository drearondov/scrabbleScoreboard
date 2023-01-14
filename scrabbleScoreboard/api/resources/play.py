from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from http import HTTPStatus
from pathlib import Path
from sqlalchemy import asc
from webargs import fields
from webargs.flaskparser import use_kwargs

from scrabbleScoreboard.extensions import db, cache
from scrabbleScoreboard.api.schemas import PlaySchema, PlayPaginationSchema
from scrabbleScoreboard.models import Game, Language, Play, Player, Word
from scrabbleScoreboard.utils.cache import clear_cache


DOCSDIR = Path(__file__).resolve().parents[2].joinpath("docs")


class PlayResource(Resource):

    method_decorators = [jwt_required]

    @swag_from(f"{DOCSDIR}/api/play/put_by_id.yml", methods=["PUT"])
    def put(self, play_id):
        play_schema = PlaySchema(partial=True)
        modify_play = Play.query.get_or_404(play_id)
        modify_play = play_schema.load(request.json, instance=modify_play)

        db.session.commit()

        clear_cache("/plays")

        return {
            "message": "play updated",
            "play": play_schema.dump(modify_play),
        }, HTTPStatus.OK

    @swag_from(f"{DOCSDIR}/api/play/delete_by_id.yml", methods=["DELETE"])
    def delete(self, play_id):
        erase_play = Play.query.get_or_404(play_id)
        erase_play.delete_play()

        clear_cache("/plays")

        return {"message": "play deleted"}, HTTPStatus.NO_CONTENT


class PlayListResource(Resource):

    method_decorators = [jwt_required]

    @use_kwargs({"page": fields.Int(missing=1), "per_page": fields.Int(missing=20)})
    @cache.cached(timeout=60, query_string=True)
    @swag_from(f"{DOCSDIR}/api/play/get_list.yml", methods=["GET"])
    def get(self, page, per_page):
        play_schema = PlayPaginationSchema()
        plays = Play.query.order_by(asc(Play.id)).paginate(page=page, per_page=per_page)

        return play_schema.dump(plays), HTTPStatus.OK

    @swag_from(f"{DOCSDIR}/api/play/create.yml", methods=["POST"])
    def post(self):

        data = request.json

        new_play = Play.api_create_play(data)

        play_schema = PlaySchema()

        return {
            "message": "play created",
            "play": play_schema.dump(new_play),
        }, HTTPStatus.CREATED


class PlaysGameListResource(Resource):
    @jwt_required
    @use_kwargs({"page": fields.Int(missing=1), "per_page": fields.Int(missing=20)})
    @cache.cached(timeout=60, query_string=True)
    @swag_from(f"{DOCSDIR}/api/play/get_list_by_game.yml", methods=["GET"])
    def get(self, game_id, page, per_page):
        play_schema = PlayPaginationSchema()
        game = Game.query.get_or_404(game_id)
        plays = Play.get_by_game(game, page, per_page)

        return play_schema.dump(plays), HTTPStatus.OK


class PlaysPlayerListResource(Resource):
    @jwt_required
    @use_kwargs({"page": fields.Int(missing=1), "per_page": fields.Int(missing=20)})
    @cache.cached(timeout=60, query_string=True)
    @swag_from(f"{DOCSDIR}/api/play/get_list_by_player.yml", methods=["GET"])
    def get(self, player_id, page, per_page):
        player = Player.query.get_or_404(player_id)
        player_schema = PlayPaginationSchema()
        plays = Play.get_by_player(player=player, page=page, per_page=per_page)

        return player_schema.dump(plays), HTTPStatus.OK

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from http import HTTPStatus
from pathlib import Path
from sqlalchemy import asc
from webargs import fields
from webargs.flaskparser import use_kwargs


from scrabbleScoreboard.api.schemas import GameSchema, GamePaginationSchema
from scrabbleScoreboard.models import Game
from scrabbleScoreboard.extensions import db, cache
from scrabbleScoreboard.utils.cache import clear_cache


DOCSDIR = Path(__file__).resolve().parents[2].joinpath("docs")


class GameResource(Resource):

    method_decorators = [jwt_required]

    @swag_from(f"{DOCSDIR}/api/game/put_by_id.yml", methods=["PUT"])
    def put(self, game_id):
        game_schema = GameSchema(partial=True)
        game = Game.query.get_or_404(game_id)
        game = game_schema.load(request.json, instance=game)

        db.session.commit()

        clear_cache("/games")

        return {
            "message": "game updated",
            "game": game_schema.dump(game),
        }, HTTPStatus.OK

    @swag_from(f"{DOCSDIR}/api/game/delete_by_id.yml", methods=["DELETE"])
    def delete(self, game_id):
        game_erase = Game.query.get_or_404(game_id)
        db.session.delete(game_erase)
        db.session.commit()

        clear_cache("/games")

        return {"message": "game deleted"}, HTTPStatus.NO_CONTENT


class GameListResource(Resource):

    method_decorators = [jwt_required]

    @use_kwargs({'page': fields.Int(missing=1), 'per_page': fields.Int(missing=20)})
    @cache.cached(timeout=60, query_string=True)
    @swag_from(f"{DOCSDIR}/api/game/get_list.yml", methods=["GET"])
    def get(self, page, per_page):
        game_schema = GamePaginationSchema()
        game_list = Game.query.order_by(asc(Game.id)).paginate(page=page, per_page=per_page)
        return game_schema.dump(game_list), HTTPStatus.OK

    @swag_from(f"{DOCSDIR}/api/game/create.yml", methods=["POST"])
    def post(self):
        game_schema = GameSchema()
        new_game = game_schema.load(request.json)

        db.session.add(new_game)
        db.session.commit()

        return {
            "message": "game created",
            "game": game_schema.dump(new_game),
        }, HTTPStatus.CREATED

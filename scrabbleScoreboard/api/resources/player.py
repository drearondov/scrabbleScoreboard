from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from http import HTTPStatus
from pathlib import Path
from webargs import fields
from webargs.flaskparser import use_kwargs

from scrabbleScoreboard.extensions import db, cache
from scrabbleScoreboard.api.schemas import PlayerSchema, PlayerPaginationSchema
from scrabbleScoreboard.models import Player
from scrabbleScoreboard.utils.cache import clear_cache


DOCSDIR = Path(__file__).resolve().parents[2].joinpath("docs")


class PlayerResource(Resource):

    method_decorators = [jwt_required]

    @cache.cached(timeout=60, query_string=True)
    @swag_from(f"{DOCSDIR}/api/player/get_by_id.yml", methods=["GET"])
    def get(self, player_id):
        player_schema = PlayerSchema()
        player = Player.query.get_or_404(player_id)

        return player_schema.dump(player), HTTPStatus.OK

    @swag_from(f"{DOCSDIR}/api/player/put_by_id.yml", methods=["PUT"])
    def put(self, player_id):
        player_schema = PlayerSchema(partial=True)
        player = Player.query.get_or_404(player_id)
        player = player_schema.load(request.json, instance=player)

        db.session.commit()

        clear_cache("/players")

        return {
            "message": "player updated",
            "player": player_schema.dump(player),
        }, HTTPStatus.OK

    @swag_from(f"{DOCSDIR}/api/player/delete_by_id.yml", methods=["DELETE"])
    def delete(self, player_id):
        erase_player = Player.query.get_or_404(player_id)
        db.session.delete(erase_player)
        db.session.commit()

        clear_cache("/players")

        return {"message": "user deleted"}, HTTPStatus.NO_CONTENT


class PlayerListResource(Resource):

    method_decorators = [jwt_required]

    @use_kwargs({'page': fields.Int(missing=1), 'per_page': fields.Int(missing=20)})
    @cache.cached(timeout=60, query_string=True)
    @swag_from(f"{DOCSDIR}/api/player/get_list.yml", methods=["GET"])
    def get(self, page, per_page):
        player_schema = PlayerPaginationSchema()
        players = Player.query.paginate(page=page, per_page=per_page)

        return player_schema.dump(players), HTTPStatus.OK

    @swag_from(f"{DOCSDIR}/api/player/create.yml", methods=["POST"])
    def post(self):
        player_schema = PlayerSchema()
        new_player = player_schema.load(request.json)

        db.session.add(new_player)
        db.session.commit()

        return {
            "message": "player created",
            "player": player_schema.dump(new_player),
        }, HTTPStatus.CREATED

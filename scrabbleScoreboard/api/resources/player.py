from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from http import HTTPStatus

from scrabbleScoreboard.extensions import db
from scrabbleScoreboard.api.schemas import PlayerSchema
from scrabbleScoreboard.models import Player


class PlayerResource(Resource):

    method_decorators = [jwt_required]

    def put(self, player_id):
        player_schema = PlayerSchema(partial=True)
        player = Player.query.get_or_404(player_id)
        player = player_schema.load(request.json, instance=player)

        db.session.commit()

        return {"message": "player updates", "player": player_schema.dump(player)}, HTTPStatus.OK


    def delete(self, player_id):
        erase_player = Player.query.get_or_404(player_id)
        db.session.delete(erase_player)
        db.session.commit()

        return {"message": "user deleted"}, HTTPStatus.NO_CONTENT


class PlayerListResource(Resource):

    method_decorators = [jwt_required]

    @swag_from("docs/player_list_get.yml")
    def get(self):
        player_schema = PlayerSchema(many=True)
        players = Player.query.all()

        return player_schema.dump(players), HTTPStatus.OK


    def post(self):
        player_schema = PlayerSchema()
        new_player = player_schema.load(request.json)
        
        db.session.add(new_player)
        db.session.commit()

        return {"message": "player created", "player": player_schema.dump(new_player)}, HTTPStatus.CREATED
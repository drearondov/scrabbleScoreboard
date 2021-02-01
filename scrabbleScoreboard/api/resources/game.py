from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from scrabbleScoreboard.api.schemas import GameSchema
from scrabbleScoreboard.models import Game
from scrabbleScoreboard.extensions import db


class GameResource(Resource):

    method_decorators = [jwt_required]

    def put(self, game_id):
        game_schema = GameSchema(partial=True)
        game = Game.query.get_or_404(game_id)
        game = game_schema.load(request.json, instance=game)

        db.session.commit()

        return {
            "message": "game updated",
            "game": game_schema.dump(game),
        }, HTTPStatus.OK

    def delete(self, game_id):
        game_erase = Game.query.get_or_404(game_id)
        db.session.delete(game_erase)
        db.session.commit()

        return {"message": "game deleted"}, HTTPStatus.NO_CONTENT


class GameListResource(Resource):

    method_decorators = [jwt_required]

    def get(self):
        game_schema = GameSchema(many=True)
        game_list = Game.query.all()
        return game_schema.dump(game_list), HTTPStatus.OK

    def post(self):
        game_schema = GameSchema()
        new_game = game_schema.load(request.json)

        db.session.add(new_game)
        db.session.commit()

        return {
            "message": "user created",
            "game": game_schema.dump(new_game),
        }, HTTPStatus.CREATED

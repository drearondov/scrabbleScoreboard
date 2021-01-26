from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from scrabbleScoreboard.extensions import db
from scrabbleScoreboard.api.schemas import PlaySchema
from scrabbleScoreboard.models import Game, Language, Play, Player

class PlayResource(Resource):

    method_decorators = [jwt_required]

    def put(self, play_id):
        play_schema = PlaySchema(partial=True)
        modify_play = Play.query.get_or_404(play_id)
        modify_play = play_schema.load(request.json, instance=modify_play)

        db.session.commit()

        return {"message": "play updated", "play": play_schema.dump(modify_play)}, HTTPStatus.CREATED

    def  delete(self, play_id):
        erase_play = Play.query.get_or_404(play_id)
        db.session.delete(erase_play)
        db.session.commit()

        return {"message": "play deleted"}, HTTPStatus.NO_CONTENT

class PlayListResource(Resource):

    method_decorators = [jwt_required]

    def get(self):
        play_schema = PlaySchema(many=True)
        plays = Play.query

        return play_schema.dump(plays), HTTPStatus.OK

    def post(self):
        word = Word.get_by_word(word=request.json['word'])
        game = Game.get_by_date(date=request.json['date'])
        player = Player.get_by_name(name=request.json['player'])
        language = Language.get_by_language(language=request.json['language'])

        if word == None:
            word = Word(word = request.json['word'], language = language)
            word.save()
        else:
            word.update_word_count()

        play_schema = PlaySchema()

        new_play = Play(
            turn_number = request.json['turn'],
            score = request.json['score'],
            word = word,
            game = game,
            player = player
        )
        new_play.save()

        return {"message": "play created", "play": play_schema.dump(new_play)}, HTTPStatus.CREATED

class PlaysGameListResource(Resource):

    @jwt_required
    def get(self, game_date):
        game = Game.get_by_date(game_date)

        play_schema = PlaySchema(many=True)
        plays = Play.get_by_game(game)

        return {"plays": play_schema.dump(plays)}, HTTPStatus.OK

class PlaysPlayerListResource(Resource):

    @jwt_required
    def get(self, player_name):
        player = Player.get_by_name(player_name)

        player_schema = PlaySchema(many=True)
        plays = Play.get_by_player(player=player)

        return {"plays": player_schema.dump(plays)}, HTTPStatus.OK

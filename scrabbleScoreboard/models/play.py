from http import HTTPStatus

from scrabbleScoreboard.extensions import db
from scrabbleScoreboard.models import Language, Word, Game, Player


class Play(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turn_number = db.Column(db.Integer)
    score = db.Column(db.Integer)
    cumulative_score = db.Column(db.Integer, default=0)

    word_id = db.Column(db.Integer, db.ForeignKey("word.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)

    def __repr__(self) -> str:
        return f"word: {self.word_id}, score: {self.score}"

    @classmethod
    def create_play(cls, data):

        try:
            word = Word.get_by_word(word=data["word"])
            game = Game.get_by_date(date=data["date"])
            player = Player.get_by_name(name=data["player"])
            language = Language.get_by_name(language_name=data["language"])
        except KeyError:
            return {
                "message": "A field in the data sent is missing, check values"
            }, HTTPStatus.BAD_REQUEST

        if word is None:
            word = Word(word=data["word"], language=language)
            word.save()
        else:
            word.update_word_count()

        last_play = (
            cls.query.filter_by(game_id=game.id).order_by(Play.id.desc()).first()
        )

        if last_play is None:
            cumulative_score = data["score"]
        else:
            cumulative_score = last_play.cumulative_score + data["score"]


        new_play = cls(
            turn_number=data["turn_number"],
            score=data["score"],
            word=word,
            game=game,
            player=player,
            cumulative_score=cumulative_score,
        )
        new_play.save_play()

        return(new_play)

    @classmethod
    def get_by_player(cls, player, page, per_page):
        return cls.query.filter_by(player=player).paginate(page=page, per_page=per_page)

    @classmethod
    def get_by_game(cls, game, page, per_page):
        return cls.query.filter_by(game=game).paginate(page=page, per_page=per_page)

    def delete_play(self):
        db.session.delete(self)
        db.session.commit()

    def save_play(self):
        db.session.add(self)
        db.session.commit()

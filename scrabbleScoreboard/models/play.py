from scrabbleScoreboard.extensions import db


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

from scrabbleScoreboard.extensions import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    avatar = db.Column(db.Integer)

    won_games = db.relationship("Game", backref="winner", lazy=True)
    plays = db.relationship("Play", backref="player", lazy=True)

    def __repr__(self) -> str:
        return f"Player {self.name}"

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first_or_404()

    def save(self):
        db.session.add(self)
        db.session.commit()

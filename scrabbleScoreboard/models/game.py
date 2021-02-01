import enum

from scrabbleScoreboard.extensions import db
from datetime import datetime as dt


class GametypeEnum(enum.Enum):
    normal = "normal"
    timed = "timed"


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=dt.now, nullable=False)
    gametype = db.Column(
        db.Enum(GametypeEnum), default=GametypeEnum.normal, nullable=False
    )

    plays = db.relationship("Play", backref="game", lazy=True)

    def __repr__(self) -> str:
        return f"<Game {self.gametype} {self.date}"

    @classmethod
    def get_by_date(cls, date):
        new_date = dt.strptime(date, "%Y-%m-%dT%H:%M:%S")
        return cls.query.filter_by(date=new_date).first_or_404()

    def save(self):
        db.session.add(self)
        db.session.commit()

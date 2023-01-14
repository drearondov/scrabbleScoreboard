import enum
from datetime import datetime as dt

from scrabbleScoreboard.extensions import db


game_players = db.Table(
    "game_players",
    db.Column("game_id", db.Integer, db.ForeignKey("game.id"), primary_key=True),
    db.Column("player_id", db.Integer, db.ForeignKey("player.id"), primary_key=True),
)


class GametypeEnum(enum.Enum):
    normal = "normal"
    timed = "timed"


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=dt.now, nullable=False)
    gametype = db.Column(
        db.Enum(GametypeEnum), default=GametypeEnum.normal, nullable=False
    )
    is_active = db.Column(db.Boolean(name="is_active"), default=False)

    winner_id = db.Column(db.Integer, db.ForeignKey("player.id"))

    plays = db.relationship("Play", backref="game", lazy=True)
    players = db.relationship(
        "Player",
        secondary=game_players,
        lazy="subquery",
        backref=db.backref("games", lazy=True),
    )

    def __repr__(self) -> str:
        return f"<Game {self.gametype} {self.date}"

    @classmethod
    def get_by_date(cls, date):
        new_date = dt.strptime(date, "%Y-%m-%dT%H:%M:%S")
        return cls.query.filter_by(date=new_date).first_or_404()

    def set_winner(self) -> None:
        player_scores = {}

        for player in self.players:
            player_scores[player.name] = []

            for play in self.plays:
                if play.player == player:
                    player_scores[player.name].append(play.cumulative_score)

            player_scores[player.name] = max(player_scores[player.name])

        winner_name = max(player_scores, key=lambda key: player_scores[key])

        for player in self.players:
            if player.name == winner_name:
                self.winner = player

    def save(self):
        db.session.add(self)
        db.session.commit()

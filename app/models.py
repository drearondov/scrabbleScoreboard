from app import db
from datetime import datetime


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), unique=True)
    times_used = db.Column(db.Integer, default=1)

    language = db.Column(db.Integer, db.ForeignKey('language.id'))
    word_plays = db.relationship('Play', backref='word_play', lazy=True)

    def __repr__(self) -> str:
        return f'<Word {self.word}>'

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(60), unique=True)

    words = db.relationship('Word', backref='word_language', lazy=True)

    def __repr__(self) -> str:
        return f'<Language {self.language}>'

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now, nullable=False)

    game_type = db.Column(db.Integer, db.ForeignKey('gametype.id'), nullable=False)
    game_plays = db.relationship('Play', backref='game_plays', lazy=True)

    def __repr__(self) -> str:
        return f'<Game {self.game_type} {self.date}'

class Gametype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_type = db.Column(db.String(60), unique=True)

    games = db.relationship('Game', backref='gametype', lazy=True)

    def __repr__(self) -> str:
        return f'<Type {self.game_type}>'

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    player_plays = db.relationship('Play', backref='player_plays', lazy=True)

    def __repr__(self) -> str:
        return f'Player {self.name}'

class Play(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    turn_number = db.Column(db.Integer)
    score = db.Column(db.Integer)

    word = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    game = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    player = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)

    def __repr__(self) -> str:
        return f'word: {self.word_id}, score: {self.score}'
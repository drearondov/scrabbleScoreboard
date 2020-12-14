from app import app, db
from app.models import Word, Language, Game, Gametype, Player, Play

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Word': Word,
        'Language': Language,
        'Game': Game,
        'Gametype': Gametype,
        'Player': Player,
        'Play': Play
    }
from scrabbleScoreboard.models import Play
from scrabbleScoreboard.extensions import ma, db


class PlaySchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    turn_number = ma.Int(required=True)
    score = ma.Int(required=True)

    word = ma.Nested('WordSchema', required=True)
    game = ma.Nested('GameSchema', required=True)
    player = ma.Nested('PlayerSchema', required=True)

    class Meta:
        model = Play
        sqla_session = db.session
        load_instance = True
        include_fk = True
        include_relationships = True
        exclude = ("word_id", "game_id", "player_id")

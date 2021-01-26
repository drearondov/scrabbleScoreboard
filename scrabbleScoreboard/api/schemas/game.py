from scrabbleScoreboard.models import Game
from scrabbleScoreboard.extensions import ma, db


class GameSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    date = ma.Date(required=True)

    plays = ma.Nested('PlaySchema', many=True)

    class Meta:
        model = Game
        sqla_session = db.session
        load_instance = True
        include_fk = True
        include_relationships = True

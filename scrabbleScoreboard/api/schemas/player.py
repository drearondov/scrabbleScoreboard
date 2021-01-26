from scrabbleScoreboard.models import Player
from scrabbleScoreboard.extensions import ma, db


class PlayerSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    name = ma.String(required=True)

    plays = ma.Nested('PlaySchema', many=True)

    class Meta:
        model = Player
        sqla_session = db.session
        load_instance = True
        include_relationships = True

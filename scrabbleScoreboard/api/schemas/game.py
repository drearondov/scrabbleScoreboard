from datetime import datetime
from marshmallow import validates, ValidationError
from marshmallow_enum import EnumField

from scrabbleScoreboard.models import Game, GametypeEnum
from scrabbleScoreboard.extensions import ma, db
from scrabbleScoreboard.utils.pagination import PaginationSchema


class GameSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    date = ma.DateTime(required=True)
    gametype = EnumField(GametypeEnum, by_value=True, required=True)

    winner = ma.Nested("PlayerSchema")

    players = ma.Nested("PlayerSchema", many=True)
    plays = ma.Nested("PlaySchema", many=True)

    @validates("date")
    def validate_date(self, date):
        if date > datetime.now():
            raise ValidationError("Date cannot be in the future")

    class Meta:
        model = Game
        sqla_session = db.session
        load_instance = True
        include_fk = True
        include_relationships = True


class GamePaginationSchema(PaginationSchema):
    data = ma.Nested("GameSchema", attribute="items", many=True)

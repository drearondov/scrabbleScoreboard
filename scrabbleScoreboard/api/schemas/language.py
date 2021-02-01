from marshmallow import RAISE

from scrabbleScoreboard.models import Language
from scrabbleScoreboard.extensions import ma, db


class LanguageSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    name = ma.String(required=True)
    code = ma.String()

    class Meta:
        model = Language
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        unknown = RAISE

from marshmallow import RAISE

from scrabbleScoreboard.models import Word
from scrabbleScoreboard.extensions import ma, db
from scrabbleScoreboard.utils.pagination import PaginationSchema


class WordSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Integer(dump_only=True)
    word = ma.String(required=True)

    language = ma.Nested("LanguageSchema", required=True)

    class Meta:
        model = Word
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True
        unknown = RAISE


class WordPaginationSchema(PaginationSchema):
    data = ma.Nested("WordSchema", attribute="items", many=True)

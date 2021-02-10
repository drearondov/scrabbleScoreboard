from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from http import HTTPStatus
from pathlib import Path
from webargs import fields
from webargs.flaskparser import use_kwargs

from scrabbleScoreboard.api.schemas import WordPaginationSchema
from scrabbleScoreboard.models import Word, Language
from scrabbleScoreboard.extensions import cache


DOCSDIR = Path(__file__).resolve().parents[2].joinpath("docs")


class WordListResource(Resource):
    """
    Multiple object resource, get_all
    """

    @jwt_required
    @use_kwargs({"page": fields.Int(missing=1), "per_page": fields.Int(missing=20)})
    @cache.cached(timeout=60, query_string=True)
    @swag_from(f"{DOCSDIR}/api/word/get_list.yml", methods=["GET"])
    def get(self, page, per_page):
        words_schema = WordPaginationSchema()
        words = Word.query.paginate(page=page, per_page=per_page)
        return words_schema.dump(words), HTTPStatus.OK


class WordLanguageListResource(Resource):
    """
    Multiple object resource
    """

    @jwt_required
    @use_kwargs({"page": fields.Int(missing=1), "per_page": fields.Int(missing=20)})
    @cache.cached(timeout=60, query_string=True)
    @swag_from(f"{DOCSDIR}/api/word/get_list_by_language.yml", methods=["GET"])
    def get(self, language_name, page, per_page):
        words_schema = WordPaginationSchema()
        selected_language = Language.get_by_name(language_name)
        language_words = Word.get_by_language(
            selected_language, page=page, per_page=per_page
        )
        return words_schema.dump(language_words), HTTPStatus.OK

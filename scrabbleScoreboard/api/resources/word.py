from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from scrabbleScoreboard.api.schemas import WordSchema
from scrabbleScoreboard.models import Word


class WordListResource(Resource):
    """
    Multiple object resource, get_all
    """

    @jwt_required
    def get(self):
        words_schema = WordSchema(many=True)
        words = Word.query.all()
        return {"words": words_schema.dump(words)}, HTTPStatus.OK

class WordLanguageListResource(Resource):
    """
    Multiple object resource
    """
    @jwt_required
    def get(self):
        words_schema = WordSchema(many=True)
        language_words = Word.get_by_language(request.json['language'])
        return {"language words": words_schema.dump(language_words)}, HTTPStatus.OK

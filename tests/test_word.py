from flask import url_for
from http import HTTPStatus

from scrabbleScoreboard.models import Word, Language
from scrabbleScoreboard.api.schemas import WordSchema


class TestWordList:

    def test_get_all_words(self, client, db, admin_headers):
        word_url = url_for('api.words')

        rep = client.get(word_url, headers=admin_headers)
        assert rep.status_code == HTTPStatus.OK

        words = db.session.query(Word).all()

        word_schema = WordSchema(many=True)
        words_serialized = word_schema.dump(words)

        results = rep.get_json()["data"]
        for word in results:
            assert word in words_serialized


    def test_get_words_by_language(self, client, db, admin_headers):
        # Test 404
        word_url = url_for('api.words_in_language', language_name="ghskusdb")
        rep = client.get(word_url, headers=admin_headers)
        assert rep.status_code == HTTPStatus.NOT_FOUND

        language = db.session.query(Language).first()
        words = db.session.query(Word).all()

        word_url = url_for('api.words_in_language', language_name=language.name)
        rep = client.get(word_url, headers=admin_headers)
        assert rep.status_code == HTTPStatus.OK

        word_schema = WordSchema(many=True)
        words_language = [word for word in words if word.language == language]
        words_serialized = word_schema.dump(words_language)

        results = rep.get_json()["data"]
        for word in results:
            assert word in words_serialized

from flask import url_for
from http import HTTPStatus

from scrabbleScoreboard.models import Word, Language


def test_get_all_words(client, mock_db, admin_headers):
    word_url = url_for('api.words')

    rep = client.get(word_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.OK

    words = mock_db.session.query(Word).all()

    results = rep.get_json()["words"]
    for word in words:
        assert any(w["id"] == word.id for w in results)


def test_get_words_by_language(client, mock_db, admin_headers):
    # Test 404
    word_url = url_for('api.words_in_language', language_name="ghskusdb")
    rep = client.get(word_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.NOT_FOUND

    language = mock_db.session.query(Language).first()
    words = mock_db.session.query(Word).all()

    word_url = url_for('api.words_in_language', language_name=language.name)
    rep = client.get(word_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.OK

    results = rep.get_json()[f"{language.name}_words"]
    words_language = [word for word in words if word.language == language]
    for word in words_language:
        assert any(w["id"] == word.id for w in results)

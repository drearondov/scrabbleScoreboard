from flask import url_for
from http import HTTPStatus

from scrabbleScoreboard.models import Play, Game, Player
from scrabbleScoreboard.api.schemas import PlaySchema


def test_put_play(client, db, admin_headers):
    # test 404
    play_url = url_for('api.play_by_id', play_id=1000000)
    rep = client.put(play_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.NOT_FOUND

    play = db.session.query(Play).order_by(Play.id.desc()).first()

    data = {
        "score": 20,
        "turn_number": 5
    }

    # test update play
    play_url = url_for('api.play_by_id', play_id=play.id)
    rep = client.put(play_url, json=data, headers=admin_headers)
    assert rep.status_code == HTTPStatus.OK

    data = rep.get_json()["play"]
    assert data["score"] == 20
    assert data["turn_number"] == 5

    db.session.refresh(play)


def test_delete_play(client, db, admin_headers):
    # test 404
    play_url = url_for('api.play_by_id', play_id=1000000)
    rep = client.delete(play_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.NOT_FOUND

    play = db.session.query(Play).order_by(Play.id.desc()).first()

    # test get play after deletion
    play_url = url_for('api.play_by_id', play_id=play.id)
    rep = client.delete(play_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.NO_CONTENT
    assert db.session.query(Play).get(play.id) is None


def test_create_play(client, db, word_factory, play, admin_headers):
    # test bad data
    play_url = url_for('api.plays')
    data = {}
    rep = client.post(play_url, json=data, headers=admin_headers)
    assert rep.status_code == HTTPStatus.BAD_REQUEST

    word = word_factory.build()
    play.word = word

    play_schema = PlaySchema()
    play = play_schema.dump(play)

    new_play = {
        "word": play["word"]["word"],
        "date": play["game"]["date"],
        "player": play["player"]["name"],
        "language": play["word"]["language"]["name"],
        "turn_number": play["turn_number"],
        "score": play["score"]
    }

    rep = client.post(play_url, json=new_play, headers=admin_headers)
    assert rep.status_code == HTTPStatus.CREATED


def test_get_all_plays(client, db, admin_headers):
    play_url = url_for('api.plays')

    plays = db.session.query(Play).all()

    rep = client.get(play_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.OK

    results = rep.get_json()["plays"]
    for play in plays:
        assert any(p["id"] == play.id for p in results)


def test_get_game_plays(client, db, admin_headers):
    # test 404
    play_url = url_for('api.plays_from_game', game_id=1000000)
    rep = client.get(play_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.NOT_FOUND

    game = db.session.query(Game).first()
    plays = db.session.query(Play).all()

    play_url = url_for('api.plays_from_game', game_id=game.id)
    rep = client.get(play_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.OK

    results = rep.get_json()["plays"]
    plays_game = [play for play in plays if play.game == game]
    for play in plays_game:
        assert any(p["id"] == play.id for p in results)


def test_get_player_plays(client, db, admin_headers):
    # test 404
    play_url = url_for('api.plays_by_player', player_id=1000000)
    rep = client.get(play_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.NOT_FOUND

    player = db.session.query(Player).first()
    plays = db.session.query(Play).all()

    play_url = url_for('api.plays_by_player', player_id=player.id)
    rep = client.get(play_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.OK

    results = rep.get_json()["plays"]
    plays_player = [play for play in plays if play.player == player]
    for play in plays_player:
        assert any(p["id"] == play.id for p in results)

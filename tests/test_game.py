from datetime import datetime
from flask import url_for
from http import HTTPStatus

from scrabbleScoreboard.models import Game, GametypeEnum


def test_put_game(client, db, game, admin_headers):
    # test 404
    game_url = url_for('api.game_by_id', game_id=1000000)
    rep = client.put(game_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.NOT_FOUND

    db.session.add(game)
    db.session.commit()

    new_data = {"date": str(datetime(2020, 12, 31))}

    # test updated game
    game_url = url_for('api.game_by_id', game_id=game.id)
    rep = client.put(game_url, json=new_data, headers=admin_headers)
    assert rep.status_code == HTTPStatus.OK

    data = rep.get_json()["game"]
    assert data["date"] == '2020-12-31T00:00:00'

    db.session.refresh(game)


def test_delete_game(client, db, game, admin_headers):
    # test 404
    game_url = url_for('api.game_by_id', game_id=1000000)
    rep = client.delete(game_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.NOT_FOUND

    db.session.add(game)
    db.session.commit()

    # test get game after deletion
    game_url = url_for('api.game_by_id', game_id=game.id)
    rep = client.delete(game_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.NO_CONTENT
    assert db.session.query(Game).filter_by(id=game.id).first() is None


def test_create_game(client, db, admin_headers):
    # test bad data
    game_url = url_for('api.games')
    data = {
        "date": str(datetime(2022, 12, 31)),
        "gametype": 'normal'
    }
    rep = client.post(game_url, json=data, headers=admin_headers)
    assert rep.status_code == HTTPStatus.BAD_REQUEST

    data["date"] = str(datetime(2020, 6, 29))

    rep = client.post(game_url, json=data, headers=admin_headers)
    assert rep.status_code == HTTPStatus.CREATED

    data = rep.get_json()
    game = db.session.query(Game).filter_by(id=data["game"]["id"]).first()

    assert game.date == datetime(2020, 6, 29)
    assert game.gametype == GametypeEnum.normal


def test_get_all_games(client, db, game_factory, admin_headers):
    game_url = url_for('api.games')
    games = game_factory.create_batch(30)

    db.session.add_all(games)
    db.session.commit()

    rep = client.get(game_url, headers=admin_headers)
    assert rep.status_code == HTTPStatus.OK

    results = rep.get_json()
    for game in games:
        assert any(g["id"] == game.id for g in results)

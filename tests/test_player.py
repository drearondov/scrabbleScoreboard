from flask import url_for
from http import HTTPStatus

from scrabbleScoreboard.models import Player


def test_get_player(client, db, player, admin_headers) -> None:
    # test 404
    player_url = url_for('api.player_by_id', player_id = "1000000")
    rep = client.get(player_url, headers = admin_headers)
    assert rep.status_code == HTTPStatus.NOT_FOUND

    db.session.add(player)
    db.session.commit()

    # test get_player
    player_url = url_for('api.player_by_id', player_id = player.id)
    rep = client.get(player_url, headers = admin_headers)
    assert rep.status_code == HTTPStatus.OK

    data = rep.get_json()
    assert data["name"] == player.name


def test_put_player(client, db, player, admin_headers) -> None:
    # test 404
    player_url = url_for('api.player_by_id', player_id = 1000000)
    rep = client.put(player_url, headers = admin_headers)
    assert rep.status_code == HTTPStatus.NOT_FOUND

    db.session.add(player)
    db.session.commit()

    data = {"name": "updated"}

    # test update user
    player_url = url_for('api.player_by_id', player_id = player.id)
    rep = client.put(player_url, json = data, headers = admin_headers)
    assert rep.status_code == HTTPStatus.OK

    data = rep.get_json()["player"]
    assert data["name"] == "updated"

    db.session.refresh(player)


def test_delete_player(client, db, player, admin_headers):
    # test 404
    player_url = url_for('api.player_by_id', player_id = 1000000)
    rep = client.delete(player_url, headers = admin_headers)
    assert rep.status_code == HTTPStatus.NOT_FOUND

    db.session.add(player)
    db.session.commit()

    # test get player after deletion
    player_url = url_for('api.player_by_id', player_id = player.id)
    rep = client.delete(player_url, headers = admin_headers)
    assert rep.status_code == HTTPStatus.NO_CONTENT
    assert db.session.query(Player).filter_by(id = player.id).first() is None


def test_create_player(client, db, admin_headers):
    # test bad data
    player_url = url_for('api.players')
    data = {}
    rep = client.post(player_url, json = data, headers = admin_headers)
    assert rep.status_code == HTTPStatus.BAD_REQUEST

    data["name"] = "created"

    rep = client.post(player_url, json = data, headers = admin_headers)
    assert rep.status_code == HTTPStatus.CREATED

    data = rep.get_json()
    player = db.session.query(Player).filter_by(id = data["player"]["id"]).first()

    assert player.name == "created"

def test_get_all_players(client, db, player_factory, admin_headers):
    player_url = url_for('api.players')
    players = player_factory.create_batch(30)

    db.session.add_all(players)
    db.session.commit()

    rep = client.get(player_url, headers = admin_headers)
    assert rep.status_code == HTTPStatus.OK

    results = rep.get_json()
    for player in players:
        assert any(p["id"] == player.id for p in results)

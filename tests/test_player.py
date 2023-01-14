from flask import url_for
from http import HTTPStatus

from scrabbleScoreboard.models import Player
from scrabbleScoreboard.api.schemas import PlayerSchema
from tests.factories import Player, PlayerFactory


class TestPlayerSingle:
    def test_get_player(self, client, db, admin_headers):
        # test 404
        player_url = url_for('api.player_by_id', player_id="1000000")
        rep = client.get(player_url, headers=admin_headers)
        assert rep.status_code == HTTPStatus.NOT_FOUND

        player = db.session.query(Player).order_by(Player.id.desc()).first()

        # test get_player
        player_url = url_for('api.player_by_id', player_id=player.id)
        rep = client.get(player_url, headers=admin_headers)
        assert rep.status_code == HTTPStatus.OK

        data = rep.get_json()
        assert data["name"] == player.name


    def test_put_player(self, client, db, admin_headers):
        # test 404
        player_url = url_for('api.player_by_id', player_id=1000000)
        rep = client.put(player_url, headers=admin_headers)
        assert rep.status_code == HTTPStatus.NOT_FOUND

        player = db.session.query(Player).order_by(Player.id.desc()).first()

        data = {"name": "updated"}

        # test update user
        player_url = url_for('api.player_by_id', player_id=player.id)
        rep = client.put(player_url, json=data, headers=admin_headers)
        assert rep.status_code == HTTPStatus.OK

        data = rep.get_json()["player"]
        assert data["name"] == "updated"

        db.session.refresh(player)


    def test_delete_player(self, client, db, admin_headers):
        # test 404
        player_url = url_for('api.player_by_id', player_id=1000000)
        rep = client.delete(player_url, headers=admin_headers)
        assert rep.status_code == HTTPStatus.NOT_FOUND

        player = PlayerFactory.build()

        db.session.add(player)
        db.session.commit()

        # test get player after deletion
        player_url = url_for('api.player_by_id', player_id=player.id)
        rep = client.delete(player_url, headers=admin_headers)
        assert rep.status_code == HTTPStatus.NO_CONTENT
        assert db.session.query(Player).get(player.id) is None


    def test_api_create_player(self, client, db, admin_headers):
        # test bad data
        player_url = url_for('api.players')
        data = {}
        rep = client.post(player_url, json=data, headers=admin_headers)
        assert rep.status_code == HTTPStatus.BAD_REQUEST

        data["name"] = "created"

        rep = client.post(player_url, json=data, headers=admin_headers)
        assert rep.status_code == HTTPStatus.CREATED

        data = rep.get_json()
        player = db.session.query(Player).order_by(Player.id.desc()).first()

        assert player.name == "created"


class TestPlayerList:
    def test_get_all_players(self, client, db, admin_headers):
        player_url = url_for('api.players')

        players = db.session.query(Player).all()

        rep = client.get(player_url, headers=admin_headers)
        assert rep.status_code == HTTPStatus.OK

        player_schema = PlayerSchema(many=True)
        serialized_players = player_schema.dump(players)

        results = rep.get_json()["data"]
        for player in serialized_players:
            assert player in results

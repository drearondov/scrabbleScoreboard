import json
import pytest

from dotenv import load_dotenv
from pytest_factoryboy import register

from scrabbleScoreboard.models.admin import Admin
from scrabbleScoreboard.app import create_app
from scrabbleScoreboard.extensions import db as _db
from tests.factories import (
    LanguageFactory, WordFactory, GameFactory, PlayerFactory, PlayFactory
)


register(LanguageFactory)
register(WordFactory)
register(GameFactory)
register(PlayerFactory)
register(PlayFactory)


@pytest.fixture(scope="session")
def app():
    load_dotenv(".testenv")
    app = create_app(testing=True)

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture
def db(app, language_factory, word_factory, game_factory,
        player_factory, play_factory):
    _db.app = app
    _db.create_all()

    language_factory.create_batch(4)
    _db.session.commit()

    word_factory.create_batch(60)
    _db.session.commit()

    game_factory.create_batch(5)
    _db.session.commit()

    player_factory.create_batch(2)
    _db.session.commit()

    play_factory.create_batch(60)
    _db.session.commit()

    yield _db

    _db.session.rollback()
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    admin = Admin(
        admin_name='admin',
        email='admin@admin.com',
        password='admin'
    )

    db.session.add(admin)
    db.session.commit()

    return admin


@pytest.fixture
def admin_headers(admin_user, client):
    data = {
        'admin': admin_user.admin_name,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))

    return {
        'content-type': 'application/json',
        'authorization': f'Bearer {tokens["access_token"]}'
    }


@pytest.fixture
def admin_refresh_headers(admin_user, client):
    data = {
        'admin': admin_user.admin_name,
        'password': 'admin'
    }
    rep = client.post(
        'auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))

    return {
        'content-type': 'application/json',
        'authorization': f'Bearer {tokens["refresh_token"]}'
    }

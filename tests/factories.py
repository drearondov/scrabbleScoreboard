import factory
import factory.fuzzy
import json

from factory import BUILD_STRATEGY
from sqlalchemy.orm import scoped_session

from scrabbleScoreboard.models import (
    Word, Language, Game, GametypeEnum, Player, Play
)
from scrabbleScoreboard.extensions import db


with open(
    'scrabbleScoreboard/static/json/ISO-639-1-language.json', 'r'
) as languages_iso:
    language_dict = json.load(languages_iso)
language_list = [language["name"] for language in language_dict]


def languages():
    yield from db.session.query(Language).all()


def games():
    yield from db.session.query(Game).all()


def players():
    yield from db.session.query(Player).all()


class LanguageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Language
        sqlalchemy_get_or_create = ('name',)
        sqlalchemy_session = scoped_session(
            lambda: db.session, scopefunc=lambda: db.session
        )

    name = factory.fuzzy.FuzzyChoice(language_list)


class WordFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Word
        sqlalchemy_get_or_create = ('word',)
        sqlalchemy_session = scoped_session(
            lambda: db.session, scopefunc=lambda: db.session
        )

    word = factory.Faker('word')
    times_used = factory.Faker('random_number')

    language = factory.iterator(languages)


class GameFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Game
        sqlalchemy_session = scoped_session(
            lambda: db.session, scopefunc=lambda: db.session
        )

    date = factory.Faker('date_time')
    gametype = factory.fuzzy.FuzzyChoice(
        [GametypeEnum.normal, GametypeEnum.timed]
    )


class PlayerFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Player
        sqlalchemy_get_or_create = ('name',)
        sqlalchemy_session = scoped_session(
            lambda: db.session, scopefunc=lambda: db.session
        )

    name = factory.Faker('name')


class PlayFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Play
        strategy = BUILD_STRATEGY
        sqlalchemy_get_or_create = ('game', 'player',)
        sqlalchemy_session = scoped_session(
            lambda: db.session, scopefunc=lambda: db.session
        )

    turn_number = factory.Faker('random_number')
    score = factory.Faker('random_number')

    game = factory.iterator(games)
    player = factory.iterator(players)
    word = factory.SubFactory(WordFactory)

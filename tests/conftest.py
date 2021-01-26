"""
Fixtures used in tests.
"""

import json
import pytest
from datetime import datetime as dt
from dotenv import load_dotenv

from scrabbleScoreboard.models import Word, Language, Play, Player, Game, GametypeEnum
from scrabbleScoreboard.app import create_app
from scrabbleScoreboard.extensions import db as _db
from pytest_factoryboy import register


@pytest.fixture
def spanish_language():
    """Returns a Language object set to Spanish."""
    return Language(language='ESP')

@pytest.fixture
def paseo_word(spanish_language):
    """Returns a Word object with the word paseo and spanish language."""
    return Word(word='paseo', language=spanish_language)

@pytest.fixture
def new_game():
    """Returns a new Game."""
    date = dt.strptime('30/03/2020', '%d/%m/%Y')
    return Game(date=date, gametype=GametypeEnum.normal)

@pytest.fixture
def new_player():
    """Return a new Player."""
    return Player(name='You Know Who')

@pytest.fixture
def paseo_play(paseo_word, new_game, new_player):
    return Play(turn_number=1, score=20, word=paseo_word, game=new_game, player=new_player)
import pytest

from datetime import datetime

from app.models import Word, Language, Play, Player, Game, Gametype


@pytest.fixture
def spanish_language():
    """Returns a Language object set to Spanish."""
    return Language(language='ESP')

@pytest.fixture
def paseo_word(spanish_language):
    """Returns a Word object with the word paseo and spanish language."""
    return Word(word='paseo', language=spanish_language)

@pytest.fixture
def normal_gametype():
    """Returns a GameType object set to Normal."""
    return Gametype(game_type='Normal')

@pytest.fixture
def new_game(normal_gametype):
    """Returns a new Game."""
    date = datetime.strptime('30/03/2020', '%d/%m/%Y')
    return Game(date=date, game_type=normal_gametype)

@pytest.fixture
def new_player():
    """Return a new Player."""
    return Player(name='You Know Who')

@pytest.fixture
def paseo_play(paseo_word, new_game, new_player):
    return Play(turn_number=1, score=20, word=paseo_word, game=new_game, player=new_player)


def test_language(spanish_language):
    assert spanish_language.language == 'ESP'

def test_gametype(normal_gametype):
    assert normal_gametype.game_type == 'Normal'

def test_player(new_player):
    assert new_player.name == 'You Know Who'

class TestWord:
    """
    Test for the Word model.
    """
    def test_word(self, paseo_word):
        assert paseo_word.word == 'paseo'

    def test_language(self, paseo_word, spanish_language):
        assert paseo_word.language == spanish_language

class TestGame:
    """
    Test the Game model.
    """
    def test_date(self, new_game):
        assert new_game.date == datetime.strptime('30/03/2020', '%d/%m/%Y')

    def test_gametype(self, new_game, normal_gametype):
        assert new_game.game_type == normal_gametype

class TestPlay:
    """
    Test the Play Model.
    """
    def test_turn(self, paseo_play):
        assert paseo_play.turn_number == 1

    def test_score(self, paseo_play):
        assert paseo_play.score == 20

    def test_word(self, paseo_play, paseo_word):
        assert paseo_play.word == paseo_word

    def test_game(self, paseo_play, new_game):
        assert paseo_play.game == new_game

    def test_player(self, paseo_play, new_player):
        assert paseo_play.player == new_player

"""
Tests for Models module.
"""

from datetime import datetime as dt

def test_language(spanish_language):
    assert spanish_language.language == 'ESP'

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
        assert new_game.date == dt.strptime('30/03/2020', '%d/%m/%Y')

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

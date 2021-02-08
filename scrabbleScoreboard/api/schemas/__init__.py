from scrabbleScoreboard.api.schemas.word import WordSchema, WordPaginationSchema
from scrabbleScoreboard.api.schemas.language import LanguageSchema
from scrabbleScoreboard.api.schemas.game import GameSchema, GamePaginationSchema
from scrabbleScoreboard.api.schemas.play import PlaySchema, PlayPaginationSchema
from scrabbleScoreboard.api.schemas.player import PlayerSchema, PlayerPaginationSchema


__all__ = [
    "WordSchema","LanguageSchema", "GameSchema", "PlaySchema", "PlayerSchema",
    "WordPaginationSchema", "GamePaginationSchema", "PlayPaginationSchema", "PlayerPaginationSchema"
]

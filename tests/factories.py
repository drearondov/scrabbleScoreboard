import factory

from scrabbleScoreboard.models import Word, Language, Game, GametypeEnum, Player, Play, language


class LanguageFactory(factory.Factory):
    language = factory.LazyAttribute(lambda n: "%03s" %n)

    class Meta:
        model = Language


class WordFactory(factory.Factory):
    pass

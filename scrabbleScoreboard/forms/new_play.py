from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from scrabbleScoreboard.models import Game, Player


def game_players():
    current_game = Game.query.filter_by(is_active=True).first()
    return Player.query.filter_by(games=current_game).all()

class NewPlayForm(FlaskForm):
    players = QuerySelectField(
        'game_players',
        query_factory=game_players,
        blank_text='Choose player',
        validators=[DataRequired()]
    )
    turn = IntegerField('Turn', validators=[DataRequired()])
    word = StringField('Word', validators=[DataRequired()])
    score = IntegerField('Play Score', validators=[DataRequired()])
    submit = SubmitField('Add play >', validators=[DataRequired()])

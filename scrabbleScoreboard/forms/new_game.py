from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField
from wtforms.validators import DataRequired


class NewGameForm(FlaskForm):
    player_1 = StringField("player_1", validators=[DataRequired()])
    player_2 = StringField("player_2", validators=[DataRequired()])
    player_3 = StringField("player_3")
    player_4 = StringField("player_4")
    gametype = RadioField(
        "game type", validators=[DataRequired()], choices=["normal", "timed"]
    )
    submit = SubmitField("let's go!")

import click
import json

from flask.cli import AppGroup


cli = AppGroup("scrabbleScoreboard")


@cli.command("init")
def init():
    """Create new admin user"""
    from scrabbleScoreboard.config import ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD
    from scrabbleScoreboard.extensions import db
    from scrabbleScoreboard.models import Admin

    click.echo("create admin")
    admin = Admin(
        admin_name=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        password=ADMIN_PASSWORD,
        active=True,
    )
    db.session.add(admin)
    db.session.commit()
    click.echo("created admin")

@cli.command("populate_lang")
def populate_lang():
    "Populate language database"
    from scrabbleScoreboard.extensions import db
    from scrabbleScoreboard.models import Language

    with open(
    'scrabbleScoreboard/static/json/ISO-639-1-language.json', 'r'
    ) as languages_iso:
        language_dict = json.load(languages_iso)
    
    for language in language_dict:
        new_language = Language(
            name=language["name"],
            code=language["code"]
        )
        db.session.add(new_language)
        db.session.commit()

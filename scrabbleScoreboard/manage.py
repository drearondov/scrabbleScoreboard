import click

from flask.cli import AppGroup

from scrabbleScoreboard.config import ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD


cli = AppGroup('scrabbleScoreboard')

@cli.command("init")
def init():
    """Create new admin user"""
    from scrabbleScoreboard.extensions import db
    from scrabbleScoreboard.models import Admin

    click.echo("create admin")
    admin = Admin(
        admin_name = ADMIN_USERNAME,
        email = ADMIN_EMAIL,
        password = ADMIN_PASSWORD,
        active = True
    )
    db.session.add(admin)
    db.session.commit()
    click.echo("created admin")

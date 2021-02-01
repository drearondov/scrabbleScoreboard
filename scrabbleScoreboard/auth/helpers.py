"""Various helpers for auth. Mainly about tokens blacklisting
heavily inspired by
https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/database_blacklist/blacklist_helpers.py
"""

from datetime import datetime as dt

from flask_jwt_extended import decode_token
from sqlalchemy.orm.exc import NoResultFound

from scrabbleScoreboard.extensions import db
from scrabbleScoreboard.models import TokenBlacklist


def add_token_to_database(encoded_token, identity_claim):
    """Adds a new token to the database. It is not revoked when it is added.

    Args:
        encoded_token ([type]): [description]
        identity_claim (string): Configured key to get user identity
    """
    decoded_token = decode_token(encoded_token)

    jti = decoded_token["jti"]
    token_type = decoded_token["type"]
    user_identity = decoded_token[identity_claim]
    expires = dt.fromtimestamp(decoded_token["exp"])
    revoked = False

    db_token = TokenBlacklist(
        jti=jti,
        token_type=token_type,
        user_id=user_identity,
        expires=expires,
        revoked=revoked,
    )

    db.session.add(db_token)
    db.session.commit()


def is_token_revoked(decoded_token):
    """Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.

    Args:
        decoded_token ([type]): [description]
    """
    jti = decoded_token["jti"]

    try:
        token = TokenBlacklist.query.filter_by(jti=jti).first()
        return token.revoked
    except NoResultFound:
        return True


def revoke_token(token_jti, user):
    """Revokes the given token
    Since we use it only on logout that already require a valid access token,
    if token is not found we raise an exception
    """
    try:
        token = TokenBlacklist.query.filter_by(jti=token_jti, user_id=user).first()
        token.revoked = True
        db.session.commit()
    except NoResultFound:
        raise Exception(f"Could not find the token {token_jti}")

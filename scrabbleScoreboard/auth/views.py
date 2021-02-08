from flask import request, jsonify, Blueprint, current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)
from flasgger import swag_from
from http import HTTPStatus
from pathlib import Path

from scrabbleScoreboard.models import Admin
from scrabbleScoreboard.extensions import pwd_context, jwt
from scrabbleScoreboard.auth.helpers import (
    revoke_token,
    is_token_revoked,
    add_token_to_database,
)


DOCSDIR = Path(__file__).resolve().parents[1].joinpath('docs')

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.route("/login", methods=["POST"])
@swag_from(f"{DOCSDIR}/auth/login.yml")
def login():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), HTTPStatus.BAD_REQUEST

    admin = request.json.get("admin", None)
    password = request.json.get("password", None)
    if admin is None or not password:
        return (
            jsonify({"message": "Missing username or password"}),
            HTTPStatus.BAD_REQUEST,
        )

    administrator = Admin.query.filter_by(admin_name=admin).first()
    if administrator is None or not pwd_context.verify(
        password, administrator.password
    ):
        return jsonify({"message": "Bad credentials"}), HTTPStatus.BAD_REQUEST

    access_token = create_access_token(identity=administrator.id)
    refresh_token = create_refresh_token(identity=administrator.id)
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

    ret = {"access_token": access_token, "refresh_token": refresh_token}
    return jsonify(ret), HTTPStatus.OK


@blueprint.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
@swag_from(f"{DOCSDIR}/auth/refresh.yml")
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    ret = {"access_token": access_token}
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    return jsonify(ret), HTTPStatus.OK


@blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required
@swag_from(f"{DOCSDIR}/auth/revoke_access_token.yml")
def revoke_access_token():
    jti = get_raw_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), HTTPStatus.OK


@blueprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_refresh_token_required
@swag_from(f"{DOCSDIR}/auth/revoke_refresh.yml")
def revoke_refresh_token():
    jti = get_raw_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), HTTPStatus.OK


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return Admin.query.get(identity)


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)

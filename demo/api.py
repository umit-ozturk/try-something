"""API view."""
import os
import logging

from flask import Blueprint, jsonify

from demo import models


log = logging.getLogger(__name__)
api = Blueprint("api", __name__, url_prefix="/api/v1")


@api.route("/ping")
def ping():
    """Debugging endpoint, simply returns PONG."""
    return jsonify(response="PONG"), 200


@api.route("/user/<user_id>")
def user(user_id):
    """Fetch user details and return as JSON."""
    user = (
        models.db.session.query(models.Users)
        .filter(models.Users.account == user_id)
        .one_or_none()
    )

    if not user:
        log.debug("User request %r not found.", user_id)
        return jsonify(response="Not Found"), 404

    return jsonify(account=user.account, active=user.active), 200

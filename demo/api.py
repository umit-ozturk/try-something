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
    user_object = (
        models.db.session.query(models.Users)
        .filter(models.Users.account == user_id)
        .one_or_none()
    )

    if not user_object:
        log.debug("User request %r not found.", user_id)
        return jsonify(response="Not Found"), 404

    return jsonify(account=user_object.account, active=user_object.active), 200


@api.route("/scopes/featureapi")
def list_all_accounts():
    """
    List all user accounts
    :return: List of account ids, status code
    """
    account_list = (
        models.db.session.query(models.Users).filter()
    )

    if not account_list:
        log.debug("There is no account.")
        return jsonify(response="Not Found"), 404

    return jsonify(account=account_list.id), 200


@api.route("/user/status/active")
def active_user_status(user_id):
    """
    Change user status active
    :param user_id: User id
    :return:
    """
    inactive_user = (
        models.db.session.query(models.Users).filter(
            models.Users.account == user_id).filter(
            models.Users.active == "inactive").one_or_none()
    )
    if inactive_user:
        # user status değiştir
        return jsonify(account=inactive_user.account, active=inactive_user.active), 200

    log.debug("User request %r not found.", user_id)
    return jsonify(response="Not Found"), 404


@api.route("/user/status/inactive")
def inactive_user_status(user_id):
    """
    Change user status inactive
    :param user_id: User id
    :return:
    """
    active_user = (
        models.db.session.query(models.Users).filter(
            models.Users.account == user_id).filter(
            models.Users.active == "active").one_or_none()
    )
    if active_user:
        # user status değiştir
        return jsonify(account=active_user.account, active=active_user.active), 200

    log.debug("User request %r not found.", user_id)
    return jsonify(response="Not Found"), 404


@api.route("/user/status/inactive")
def order_and_status_list(user_id):
    """
    Change user status inactive
    :param user_id: User id
    :return:
    """
    user_object = (
        models.db.session.query(models.Users).filter(
            models.Users.account == user_id).one_or_none()
    )
    if user_object:
        return jsonify(account=user_object.data), 200

    log.debug("User request %r not found.", user_id)
    return jsonify(response="Not Found"), 404

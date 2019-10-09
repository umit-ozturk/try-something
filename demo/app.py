"""Application build module."""
import os
import logging
import sys
from typing import Tuple

from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # type: ignore

from demo.models import db
from demo.api import api
from demo import config

log = logging.getLogger(__name__)


def configure_app(app, testing=False) -> None:
    """Configure app with our config."""
    # http://flask.pocoo.org/docs/api/#configuration
    if testing:
        test_config = config.TestingConfig()
        log.debug("Loading testing config, %r", test_config)
        app.config.from_object(test_config)
    else:
        app.config.from_object(config.ProductionConfig())


def configure_blueprints(app) -> None:
    """Configure blueprints."""
    app.register_blueprint(api)

    def setup_models():
        log.info("Triggering model load hook.")
        # TODO: Add any pre first request hooks

    app.before_first_request(setup_models)


def configure_logging(app, testing=False) -> None:
    """Configure application logging."""
    logger = logging.getLogger()
    logger.setLevel(level=app.config["LOG_LEVEL"])

    if not testing:
        logHandler = logging.StreamHandler()
        log_format = (
            "%(asctime) %(funcName) %(levelname) %(lineno)"
            " %(message) %(name)  %(process) %(processName)"
        )
        logHandler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(logHandler)
    else:
        log.info("Started in testing mode, ignoring logging output.")


def init_production() -> Flask:
    """Create a Flask app."""
    app = Flask(__name__)
    configure_app(app)
    configure_blueprints(app)
    configure_logging(app)

    db.init_app(app)
    log.info("App started in PRODUCTION mode.")
    return app


def init_testing() -> Flask:
    """Create a Flask app."""
    app = Flask(__name__)

    configure_app(app, testing=True)
    configure_blueprints(app)
    configure_logging(app, testing=True)

    db.init_app(app)
    log.info("App started in TESTING mode.")
    return app


production = init_production
testing = init_testing

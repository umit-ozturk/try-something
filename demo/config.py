"""Configuration module."""
import os


class Config:
    """Root configuration object."""

    DEBUG = False
    TESTING = False
    LOG_LEVEL = "INFO"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Testing configuration object."""

    LOG_LEVEL = "DEBUG"
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Default to an in memory DB as we don't need one in most places.
    SQLALCHEMY_DATABASE_URI = os.environ.get("API_DB_URL")
    # SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DB_URL", ":memory:")


class ProductionConfig(Config):
    """Production configuration extracting from environment."""

    LOG_LEVEL = os.environ.get("API_LOG_LEVEL", "INFO")
    SQLALCHEMY_DATABASE_URI = os.environ.get("API_DB_URL")

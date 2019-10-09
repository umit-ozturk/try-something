import logging
import os
from pathlib import Path

import pytest  # type: ignore

from demo import app
from demo.models import db

log = logging.getLogger(__name__)


@pytest.fixture()
def integration_client(caplog, request, postgresql):
    caplog.set_level(logging.DEBUG)
    test_url = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}".format(
        user=postgresql.info.user,
        password=postgresql.info.password,
        host=postgresql.info.host,
        port=postgresql.info.port,
        dbname=postgresql.info.dbname,
    )
    # Export this so we can fetch it from tests.
    os.environ["TEST_DB_URL"] = test_url
    log.debug("Generated Postgres URL %r.", test_url)

    # Setup a test server and use our new postgres client.
    server = app.init_testing()
    server.config["SQLALCHEMY_DATABASE_URI"] = test_url
    client = server.test_client()

    # Setup our app context create the database and populate it.
    with server.app_context():
        db.create_all()

        cursor = postgresql.cursor()
        # Load all the tables we require for our tests.
        for database, path in [
            ("users", Path("tests/resources/users.csv").absolute()),
        ]:

            load_query = f"COPY {database} FROM '{path}' DELIMITER ',' CSV HEADER;"
            log.debug("Running %r against db.", load_query)
            cursor.execute(load_query)

            postgresql.commit()
            log.debug("Table %r loaded.", database)

    def finalise():
        log.debug("Clearing database.")
        with server.app_context():
            db.drop_all()

    request.addfinalizer(finalise)
    return client

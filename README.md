# Demo API

This API is just here to return some database results.  It's a simplified
version of some of the public APIs we run.  This isn't all the work we do
but is some of the simplest things that you can expect to do.


### Installation

The setup requires Python3.6 or above and the installation instructions are
written to be run inside of a virtual environment.

```sh
# Install postgresql.
sudo apt update && sudo apt install postgresql-10
# Production installation that just contains dependency packages.
python setup.py install
# Development installation that brings along test dependencies.
python setup.py develop
```

### Tests

Check everything works before you start.

```sh
black demo --check
pytest
```


### Running

To run the server locally using the development configuration (this has defaults)
but can be overriden with environment variables as per the below configuration.

```sh
# Development running on the internal flask server.
export FLASK_APP=demo.app:testing
flask run
```


### Configuration

Configuration for the app is as follows.

| Configurable     | Info                          | Environment Variable | Default |
|------------------|-------------------------------|----------------------|---------|
| Log Level        | Console log level             | API_LOG_LEVEL        | INFO    |
| API Database URL | Takes a prefixed database URL | API_DB_URL           | N/A     |

API database URL can either be a postgres or sqlite URL.


### API Docs

Basic API response docs are below.

| Path            | Method | Body | Returns                                         |
|-----------------|--------|------|-------------------------------------------------|
| /ping           | GET    | N/A  | {"response": "PONG"}                            |
| /user/<user_id> | GET    | N/A  | {"account":"example@example.org","active":true} |

Responses are standard REST responses.

- 200 for success.
- 401 for not authorized (no credentials provided).
- 404 for no record found.
- 409 for a conflict (inserting an already existing record).


### SQL and Database

The tests run with a postgres database fixture that loads a SQL file from
resources.  If you wish to load these yourself (rather than using the inbuilt tests)
then the file is in tests/resources.

Once the database has been constructed (and tables built) the following command should
load the file.  If you need to build the tables SQLAlchemy should be able to do it for
you, check the integration_client fixture as an example is there.

```sql
COPY user FROM 'tests/resources/user.csv' DELIMITER ',' CSV HEADER;
```

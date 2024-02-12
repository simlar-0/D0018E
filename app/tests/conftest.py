"""
Provides an app and database for testing.
"""
import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.db import create_db, destroy_db, execute_script, grant_privileges
from definitions import APP_DIR

# read in SQL for populating test data
#with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
#    _data_sql = f.read().decode("utf8")

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app({'MYSQL_DB':'test_db', 'MYSQL_HOST':'localhost'})

    
    # create the database and load test data
    with app.app_context():
        destroy_db(app.config['MYSQL_DB'])
        create_db(app.config['MYSQL_DB'])
        grant_privileges(app.config['MYSQL_DB'],app.config['MYSQL_USER'])
        execute_script(os.path.join(APP_DIR,'tests','data','schema.sql'))

    yield app

    with app.app_context():
        destroy_db(app.config['MYSQL_DB'])


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
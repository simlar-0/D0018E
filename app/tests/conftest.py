"""
Provides an app and database for testing.
"""
import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.db import execute_script, clear_db
from definitions import APP_DIR

# read in SQL for populating test data
#with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
#    _data_sql = f.read().decode("utf8")

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app(
        {'MYSQL_USER':'test_user',
        'MYSQL_PASSWORD':'',
        'MYSQL_DB':'test_db',
        'MYSQL_HOST':'db',
        'DEBUG':True})

    try:
        with app.app_context():
            clear_db()
            execute_script(os.path.join(APP_DIR,'sql','schema.sql'))

        yield app
    finally:
        with app.app_context():
            clear_db()


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
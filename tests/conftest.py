import os
import tempfile

import pytest
from flaskapi import create_app, mongo


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    test_settings = {
        "SECRET_KEY": "test",
        "MONGODB_DB": 'flaskydb',
        "MONGODB_HOST": '127.0.0.1',
        "MONGODB_PORT": "27017",
        "MONGODB_USERNAME": 'flaskyuser',
        "MONGODB_PASSWORD": 'secret'
    }
    app = create_app(test_settings)

    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


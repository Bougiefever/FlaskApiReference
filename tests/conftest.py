import os
import tempfile

import pytest
from flaskapi import create_app
from flaskapi import db

@pytest.fixture
def client(app):
    return app.test_client()

def runner(app):
    return app.test_cli_runner()


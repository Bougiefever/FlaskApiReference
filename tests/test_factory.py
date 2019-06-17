import pytest
from flaskapi import create_app


def test_hello(client):
    response = client.get("/hello")
    assert response.data == b"hello"

def test_config(app):
    assert app.config.get('SECRET_KEY') == 'test'
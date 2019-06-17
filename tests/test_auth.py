import pytest
import json

def test_logout(client):
    # test that successful registration redirects to the login page
    response = client.get("/auth/logout/")
    assert "hello" in response.headers["Location"]
    assert response.status_code == 302

def test_register(client, app):

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "username": "test1", "password": "pass1"
    }
    url = '/auth/register/'

    response = client.post(url, data=json.dumps(data), headers= { 'Content-Type': 'application/json' })
    print('response content type', response.content_type)
    assert response.content_type == mimetype
    assert response.json['message'] == "register post method response"
    assert response.status_code == 201


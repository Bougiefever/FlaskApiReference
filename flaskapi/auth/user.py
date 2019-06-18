from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash, check_password_hash
from flask import make_response, jsonify
from flaskapi import mongo
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError
from flask_jwt_extended import create_access_token, create_refresh_token

Users = mongo.db.users
headers = { 'Content-Type': 'application/json'}
user_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 5
        }
    },
    "required": ["username", "email", "password"],
    "additionalProperties": False
}

login_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
        },
        "password": {
            "type": "string",
            "minLength": 5
        }
    },
    "required": ["username", "password"],
    "additionalProperties": False
}

class User():
    def get(self, user):
        username = user["username"]
        spec = { "username": username}
        doc = Users.find_one(spec)
        if not doc:
            return None

        return doc

    def post(self, data):
        passwordhash = generate_password_hash(data['password'])
        user = {"username": data["username"], "email": data["email"], "pass_hash": passwordhash}
        doc = Users.insert_one(user).inserted_id
        return str(doc)

    def put(self, data, justOne=True):
        return NotImplemented

    def delete(self, data, justOne=True):
        return NotImplemented

    def authenticate_user(self, data):
        user = self.get(data)
        print('user before', user)
        if user and check_password_hash(user['pass_hash'], data['password']):
            del user['pass_hash']
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            user['token'] = access_token
            user['refresh'] = refresh_token
            print('user after', user)
            return {'ok': True, 'data': user}
        else:
            return {'ok': False, "message": "invalid username or password"}

    def validate_login(self, data):
        try:
            validate(data, login_schema)
        except ValidationError as e:
            print('validation error occured')
            return {'ok': False, 'message': e}
        except SchemaError as e:
            print('schema error occurred')
            return {'ok': False, 'message': e}
        return {'ok': True, 'data': data}

    def validate_user(self, data):
        try:
            validate(data, user_schema)
        except ValidationError as e:
            print('validation error occured')
            return {'ok': False, 'message': e}
        except SchemaError as e:
            print('schema error occurred')
            return {'ok': False, 'message': e}
        return {'ok': True, 'data': data}



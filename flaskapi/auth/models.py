from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash, check_password_hash
from flask import make_response, jsonify
from flaskapi import mongo, JSONEncoder

Users = mongo.db.users
headers = { 'Content-Type': 'application/json'}

class User():
    def get(self, username):
        spec = { "username": username}
        doc = Users.find_one(spec)
        if not doc:
            return None

        return doc

    def post(self, user):
        doc = Users.insert_one(user).inserted_id
        return str(doc)

    def put(self, payload, justOne=True):
        return NotImplemented

    def delete(self, payload, justOne=True):
        return NotImplemented

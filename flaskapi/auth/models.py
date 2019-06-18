
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash, check_password_hash
from flask import make_response, jsonify
from flaskapi import mongo
from flaskapi import Resource, representation

Users = mongo.db.users #mongo.Connection("localhost", 27017)["mydb"]["users"]
headers = { 'Content-Type': 'application/json'}

class User(Resource):

    def GET(self, request, username):
        spec = {
            "username": username,
            "_meta.active": True
        }
        # this is a simple call to pymongo - really, do
        # we need anything else?
        doc = Users.find_one(spec)
        if not doc:
            return NotFound(username)
        payload= jsonify(doc)
        return make_response(payload,  200, headers)

    def POST(self, request, username, password):
        passhash = generate_password_hash(password)
        spec = {
            "username": username,
            "passwordhash": passhash
        }
        inserted_id = mongo.db.users.insert_one(spec).inserted_id
        return make_response({"inserted_id": jsonify(inserted_id), "message": "user was successfully registered"}, 201, headers)

    def PUT(self, request, username):
        spec = {
            "username": username,
            "_meta.active": True
        }
        operation = {
            "$set": request.json,
        }
        # this call to pymongo will return the updated document (implies safe=True)
        doc = Users.update(spec, operation, new=True)
        if not doc:
            return NotFound(username)
        payload= jsonify(doc)
        return make_response(payload, 200, headers)
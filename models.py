from flaskapi import mongo

users = mongo.db.users

class User():
    def get(self, username):
        spec = { "username": username}
        doc = users.find_one(spec)
        if not doc:
            return None

        return doc

    def post(self, user):
        doc = users.insert_one(user).inserted_id
        return str(doc)

    def put(self, payload, justOne=True):
        return NotImplemented

    def delete(self, payload, justOne=True):
        return NotImplemented

def authenticate(username, password):
    pass

def identity(payload):
    pass
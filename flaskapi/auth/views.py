from flask import Blueprint, request, make_response, jsonify, g, session, redirect, url_for
from flask.views import MethodView
from http import HTTPStatus
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flaskapi import mongo
from bson.objectid import ObjectId
from flaskapi.auth.models import User, JSONEncoder

bp = Blueprint('auth', __name__, url_prefix='/auth')
headers = { 'Content-Type': 'application/json'}

users = User()

class RegisterAPI(MethodView):
    """ handle registering new users	"""

    def post(self):
        # Extract info from request body
        json_data = request.get_json()
        username = json_data["username"]
        password = json_data["password"]
        passhash = generate_password_hash(password)

        try:
            # check database to see if user already exists
            user = users.get(username=username)
            if user is None:
                # create new user doc and add to users collection
                new_user = {'username': username, 'passwordhash': passhash}
                user = users.post(user=new_user)
                response_object = { "message": "user successfully registered", "id": user}
                return make_response(jsonify(response_object), HTTPStatus.CREATED, headers)
            else:
                response_object = {"message": "user is already registerd.","user": user}
                return make_response(jsonify(response_object), HTTPStatus.ACCEPTED, headers)
        except Exception as e:
            response_object = {"message": "failure", "exeption": str(e)}
            return make_response(jsonify(response_object), HTTPStatus.INTERNAL_SERVER_ERROR, headers)


class LoginAPI(MethodView):
    def post(self):
        # Extract info from request body
        json_data = request.get_json()
        username = json_data["username"]
        password = json_data["password"]

        # get user from users collection
        user = users.get(username=username)
        print("user", user)
        if user is not None:
            passwordhash = user['passwordhash']
            is_password_match = check_password_hash(passwordhash, password)
        else:
            is_password_match = False

        if not is_password_match:
            return make_response(jsonify({"message": "user or password does not exist."}), HTTPStatus.ACCEPTED, headers)
        else:
            return make_response(jsonify({"message": "user is authenticated"}), HTTPStatus.OK, headers)


class LogoutAPI(MethodView):
    def get(self):
        session.clear()
        return make_response(jsonify({"message": "user is logged out"}), HTTPStatus.OK)

@bp.before_app_request
def flaskapi_check_user_status():
    """ Is executed before each request in app, even outside of auth bluprint
    Checks to see if the session has a user and adds it to g if found
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = { "user_id": 0, "username": "nulluser"}



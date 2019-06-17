from flask import Blueprint, request, make_response, jsonify, g, session, redirect, url_for
from flask.views import MethodView
from http import HTTPStatus
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flaskapi import mongo

bp = Blueprint('auth', __name__)

class RegisterAPI(MethodView):
    """ handle registering new users	"""

    def post(self):
        # Extract info from request body
        json_data = request.get_json()
        username = json_data["username"]
        password = json_data["password"]
        passhash = generate_password_hash(password)

        headers = { 'Content-Type': 'application/json'}

        # check database to see if user already exists
        try:
            user = mongo.db.users.find_one({'username': username})
            if user is None:
                response_object = { "message": "register post method response"}
                response = make_response(jsonify(response_object), HTTPStatus.CREATED, headers)
                return response
            else:
                response_object = {"message": "user is already registerd."}
                response = make_response(jsonify(response_object), 202, headers)
        except Exception as e:
            response_object = {"message": "failure", "exeption": str(e)}
            response = make_response(jsonify(response_object), 500, headers)

class LoginAPI(MethodView):
    def post(self):
        response_object = { "message": "login post method"}
        response = make_response(jsonify(response_object))
        return response, HTTPStatus.OK

class LogoutAPI(MethodView):
    def get(self):
        session.clear()
        return redirect(url_for('hello'))

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



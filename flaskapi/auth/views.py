from flask import Blueprint, request, make_response, jsonify, g, session, redirect, url_for
from flask.views import MethodView
from http import HTTPStatus
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flaskapi import mongo
from bson.objectid import ObjectId
from flaskapi.auth.user import User
from flask_jwt_extended import get_jwt_identity, get_current_user, create_access_token, jwt_refresh_token_required

bp = Blueprint('auth', __name__, url_prefix='/auth')
headers = { 'Content-Type': 'application/json'}

users = User()

class RegisterAPI(MethodView):
    """ handle registering new users	"""

    def post(self):
        try:
            # Extract info from request body
            data = users.validate_user(request.get_json())
            validated = data['ok']
            if not validated:
                response_object = {"message": "user data is invalid", "reason": data['message'].message}
                return make_response(jsonify(response_object), HTTPStatus.BAD_REQUEST, headers)
            new_user = data['data'] # get user object from request data

            # check database to see if user already exists
            user = users.get(new_user)
            if user is None:
                # create new user doc and add to users collection
                user = users.post(new_user)
                response_object = { "message": "user successfully registered", "id": user}
                return make_response(jsonify(response_object), HTTPStatus.CREATED, headers)
            else:
                response_object = {"message": "user is already registered.","user": user}
                return make_response(jsonify(response_object), HTTPStatus.ACCEPTED, headers)
        except Exception as e:
            response_object = {"message": "failure", "exeption": str(e)}
            return make_response(jsonify(response_object), HTTPStatus.INTERNAL_SERVER_ERROR, headers)


class LoginAPI(MethodView):
    def post(self):
        data = users.validate_login(request.get_json())
        auth_response = users.authenticate_user(data['data'])
        return(jsonify(auth_response), 200, headers)

class LogoutAPI(MethodView):
    def get(self):
        session.clear()
        return make_response(jsonify({"message": "user is logged out"}), HTTPStatus.OK)

@bp.route('/refresh/', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    ''' refresh token endpoint '''
    current_user = get_jwt_identity()
    ret = {
            'token': create_access_token(identity=current_user)
    }
    return make_response(jsonify({'ok': True, 'data': ret}), 200, headers)

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

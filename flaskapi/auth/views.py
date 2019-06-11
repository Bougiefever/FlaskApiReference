from flask import Blueprint, request, make_response, jsonify, g, session, redirect, url_for
from flask.views import MethodView

bp = Blueprint('auth', __name__)

class RegisterAPI(MethodView):
    """ handle registering new users	"""

    def post(self):
        response_object = { "message": "register post method"}
        response = make_response(jsonify(response_object))
        return response, 201

class LoginAPI(MethodView):
    def post(self):
        response_object = { "message": "login post method"}
        response = make_response(jsonify(response_object))
        return response, 200

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



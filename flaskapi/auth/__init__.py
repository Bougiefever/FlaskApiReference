from flaskapi.auth.views import bp, RegisterAPI, LoginAPI, LogoutAPI

register_view = RegisterAPI.as_view('register_api')
bp.add_url_rule('/register/', view_func=register_view, methods=['POST'])

login_view = LoginAPI.as_view('login_api')
bp.add_url_rule('/login/', view_func=login_view, methods=['POST'])

logout_view = LogoutAPI.as_view('logout_api')
bp.add_url_rule('/logout/', view_func=logout_view, methods=['GET'])
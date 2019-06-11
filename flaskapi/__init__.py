import os

from flask import Flask
import os
from dotenv import load_dotenv

def load_config(app):
    """ Loads configuration from .env file   """
    # load configuration settings
    APP_ROOT = os.path.abspath(os.path.dirname(__file__))
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)

    app.secret_key = os.getenv('SECRET_KEY')
    app.config['DATABASE_CONNECTION'] = os.getenv('MONGODB_CONNECTION_BASE') + os.getenv('DATABASE_NAME')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    load_config(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        a_setting = app.config.get('DATABASE_CONNECTION')
        return 'my db setting: {}'.format(a_setting)

    # register auth api
    from flaskapi import auth
    app.register_blueprint(auth.bp)

    return app


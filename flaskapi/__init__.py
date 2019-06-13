import os

from flask import Flask
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv

db = MongoEngine()

def load_config(app):
    """ Loads configuration from .env file   """
    # load configuration settings
    APP_ROOT = os.path.abspath(os.path.dirname(__file__))
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)

    app.secret_key = os.getenv('SECRET_KEY')
    app.config['MONGODB_DB'] = os.getenv('MONGODB_DB')
    app.config['MONGODB_HOST'] = os.getenv('MONGODB_HOST')
    app.config['MONGODB_PORT'] = os.getenv('MONGODB_PORT')
    app.config['MONGODB_USERNAME'] = os.getenv('MONGODB_USERNAME')
    app.config['MONGODB_PASSWORD'] = os.getenv('MONGODB_PASSWORD')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    load_config(app)
    db.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return "hello"

    # register auth api
    from flaskapi import auth
    app.register_blueprint(auth.bp)

    return app

